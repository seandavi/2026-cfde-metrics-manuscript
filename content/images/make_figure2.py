# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click>=8.1",
#     "pillow>=11.0",
#     "playwright>=1.50",
# ]
# ///
"""Build Figure 2: the CFDE ICC metrics dashboard as three stacked panels.

Panels
  (A) Program overview: summary counts and cumulative publications and
      award funding.
  (B) Website engagement from Google Analytics.
  (C) GitHub repositories for one core project.

The screenshot build shows the full March 2026 panels; the live capture
shows a curated subset of each (see LIVE_PANELS).

Two sources, never mixed, so every panel shows one data vintage:

  from-screenshot  Crop the three panels out of the March 2026 three-column
                   screenshot (dashboard_screenshot.png) and restack them.
                   This is the committed interim figure.
  capture          Re-capture a curated subset of the live dashboard at
                   high resolution, two cards per row, so its text stays
                   legible at print size. Panel C (project repositories)
                   needs an ORCID login, so pass a saved Playwright session
                   created with the `login` command.

Output is a 300 dpi PNG sized for Trends Open (max 12.7 cm wide with the
legend below the figure).

Run from this directory:
  uv run make_figure2.py from-screenshot
  uv run --with playwright playwright install chromium   # once
  uv run make_figure2.py login --storage-state .dashboard-auth.json
  uv run make_figure2.py capture --storage-state .dashboard-auth.json

The storage-state file holds a live login session: it is gitignored and must
never be committed.
"""

import asyncio
import datetime
from io import BytesIO
from pathlib import Path

import click
from PIL import Image, ImageChops, ImageDraw, ImageFont
from playwright.async_api import Locator, Page, async_playwright

HERE = Path(__file__).resolve().parent
DASHBOARD_URL = "https://cfde-eval.netlify.app/"
# Core project shown in panel C (the ICC's own award, as in the screenshot).
PANEL_C_PROJECT = "U54OD036472"

DPI = 300
CM_PER_INCH = 2.54
LABEL_PT = 9
LABEL_FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

# Panel boxes (left, top, right, bottom) in dashboard_screenshot.png
# (2218x893), measured from its light-blue separator gutters, as rows of
# cards. Panel C is two stacked cards in the screenshot; they are placed side
# by side here.
SCREENSHOT_PANELS: dict[str, list[list[tuple[int, int, int, int]]]] = {
    "A": [[(15, 16, 874, 876)]],
    "B": [[(899, 16, 1757, 876)]],
    "C": [[(1783, 16, 2200, 434), (1783, 459, 2200, 876)]],
}

# Live capture. A full dashboard section scaled to 12.7 cm prints its text at
# 2-3 pt, so the figure shows a curated subset: each row is at most two
# 360x270 CSS px chart cards, which puts the charts' 11 px labels near 6 pt.
# A card is (page path, section heading, CSS selector within the section,
# index among its matches, table columns to keep or None). Chart cards are
# ECharts canvases, so they are picked by position; captions are checked by
# eye in the output.
REPO_COLUMNS = ["Name", "Commits", "Issues", "PRs", "License"]
PROJECT = f"core-project/{PANEL_C_PROJECT}"
CHART = ".charts > .chart"
Card = tuple[str, str, str, int, list[str] | None]
LIVE_PANELS: dict[str, list[list[Card]]] = {
    "A": [
        [("", "Overview", "dl.details", 0, None)],
        # Over Time charts: projects, fiscal-year awards, publications.
        [("", "Over Time", CHART, 2, None), ("", "Over Time", CHART, 1, None)],
    ],
    "B": [
        # Analytics charts: active, new, returning users, engaged sessions.
        [("", "Analytics", CHART, 0, None), ("", "Analytics", CHART, 3, None)],
    ],
    "C": [
        [(PROJECT, "Repositories", "table", 0, REPO_COLUMNS)],
        # Repository charts: forks, issues, pull requests, commits.
        [(PROJECT, "Repositories", CHART, 3, None), (PROJECT, "Repositories", CHART, 1, None)],
    ],
}
VIEWPORT_WIDTH = 1200
DEVICE_SCALE_FACTOR = 3
NOT_AUTHORIZED_TEXT = "not authorized"


def cm_to_px(cm: float) -> int:
    return round(cm / CM_PER_INCH * DPI)


def pt_to_px(pt: float) -> int:
    return round(pt / 72 * DPI)


def content_mask(rgb: Image.Image, tolerance: int) -> Image.Image:
    """White where a pixel differs from its row's left-edge background colour.

    Comparing per row (rather than against one colour) handles dashboard
    sections with different background bands.
    """
    edge = rgb.crop((0, 0, 1, rgb.height)).resize(rgb.size)
    diff = ImageChops.difference(rgb, edge).convert("L")
    return diff.point([255 if v > tolerance else 0 for v in range(256)])


def trim(card: Image.Image, tolerance: int = 8, pad: int = 12) -> Image.Image:
    """Crop away background margins around a card's content."""
    rgb = card.convert("RGB")
    bbox = content_mask(rgb, tolerance).getbbox()
    if bbox is None:
        return rgb
    left, top, right, bottom = bbox
    return rgb.crop(
        (
            max(left - pad, 0),
            max(top - pad, 0),
            min(right + pad, rgb.width),
            min(bottom + pad, rgb.height),
        )
    )


def collapse_blank_rows(
    card: Image.Image, max_blank: int = 12, tolerance: int = 8
) -> Image.Image:
    """Shorten runs of blank (single-colour) rows to at most max_blank px.

    Removes only empty vertical whitespace inside a card, never content, so
    the tall dashboard panels fit on one page.
    """
    rgb = card.convert("RGB")
    mask = content_mask(rgb, tolerance)
    keep: list[int] = []
    blank_run = 0
    for y in range(rgb.height):
        if mask.crop((0, y, rgb.width, y + 1)).getbbox() is None:
            blank_run += 1
            if blank_run > max_blank:
                continue
        else:
            blank_run = 0
        keep.append(y)
    collapsed = Image.new("RGB", (rgb.width, len(keep)))
    for new_y, y in enumerate(keep):
        collapsed.paste(rgb.crop((0, y, rgb.width, y + 1)), (0, new_y))
    return collapsed


def load_label_font(size_px: int) -> ImageFont.FreeTypeFont:
    for path in LABEL_FONTS:
        if Path(path).exists():
            return ImageFont.truetype(path, size_px)
    raise click.ClickException(f"No bold sans-serif font found in {LABEL_FONTS}")


def compose(
    panels: dict[str, list[list[Image.Image]]], width_cm: float, output: Path
) -> Image.Image:
    """Stack panels and their rows, cards within a row side by side, one scale.

    Every card is scaled by the same factor, chosen so the widest row fills
    the print width; narrower rows are centred.
    """
    card_gap = 12  # source px between cards in one row
    rows = [
        (label if i == 0 else None, [collapse_blank_rows(trim(c)) for c in cards])
        for label, panel_rows in panels.items()
        for i, cards in enumerate(panel_rows)
    ]
    row_widths = [
        sum(c.width for c in cards) + card_gap * (len(cards) - 1) for _, cards in rows
    ]
    width_px = cm_to_px(width_cm)
    scale = width_px / max(row_widths)

    font = load_label_font(pt_to_px(LABEL_PT))
    label_height = round(pt_to_px(LABEL_PT) * 1.25)
    panel_gap = pt_to_px(LABEL_PT) // 2
    row_gap = round(card_gap * scale)

    scaled = [
        (
            label,
            [
                c.resize(
                    (round(c.width * scale), round(c.height * scale)),
                    Image.Resampling.LANCZOS,
                )
                for c in cards
            ],
        )
        for label, cards in rows
    ]
    height_px = sum(
        (label_height + (panel_gap if i else 0) if label else row_gap)
        + max(c.height for c in cards)
        for i, (label, cards) in enumerate(scaled)
    )

    figure = Image.new("RGB", (width_px, height_px), "white")
    draw = ImageDraw.Draw(figure)
    y = 0
    for i, ((label, cards), row_width) in enumerate(zip(scaled, row_widths)):
        if label:
            y += panel_gap if i else 0
            draw.text((0, y), f"({label})", font=font, fill="black")
            y += label_height
        else:
            y += row_gap
        x = round((width_px - row_width * scale) / 2)
        for card in cards:
            figure.paste(card, (x, y))
            x += card.width + round(card_gap * scale)
        y += max(c.height for c in cards)

    figure.save(output, dpi=(DPI, DPI))
    click.echo(
        f"Wrote {output} ({width_px}x{height_px} px = "
        f"{width_cm:.1f} x {height_px / DPI * CM_PER_INCH:.1f} cm at {DPI} dpi; "
        f"source scaled x{scale:.2f})"
    )
    return figure


async def keep_table_columns(table: Locator, columns: list[str]) -> None:
    """Hide every column of the table whose header is not listed; fit the rest."""
    missing = await table.evaluate(
        """(table, keep) => {
            const headers = [...table.querySelectorAll('thead th')]
                .map(th => th.textContent.trim());
            const hide = new Set();
            headers.forEach((h, i) => { if (!keep.includes(h)) hide.add(i); });
            for (const row of table.querySelectorAll('tr')) {
                [...row.children].forEach((cell, i) => {
                    if (hide.has(i)) cell.style.display = 'none';
                    // Wrap long cells (licence names) instead of widening.
                    cell.style.maxWidth = '14em';
                    cell.style.whiteSpace = 'normal';
                });
            }
            // Size the table to its remaining columns, not the page width.
            table.style.width = 'auto';
            return keep.filter(h => !headers.includes(h));
        }""",
        columns,
    )
    if missing:
        raise click.ClickException(f"Table has no column(s) {missing}")


async def capture_card(page: Page, card: Card) -> Image.Image:
    """Screenshot one element of a dashboard section."""
    _, heading, selector, index, columns = card
    section = page.locator(f'main > section:has(> h2:text-is("{heading}"))')
    if NOT_AUTHORIZED_TEXT in (await section.inner_text()).lower():
        raise click.ClickException(
            f"Section {heading!r} at {page.url} is login-only. Run the "
            "`login` command and pass its --storage-state file."
        )
    element = section.locator(selector).nth(index)
    if columns is not None:
        await keep_table_columns(element, columns)
    await element.scroll_into_view_if_needed()
    clipped = await element.evaluate(
        """e => [e, ...e.querySelectorAll('*'), e.parentElement].some(x =>
            x.scrollWidth > x.clientWidth + 2 &&
            getComputedStyle(x).overflowX !== 'visible')"""
    )
    if clipped:
        raise click.ClickException(
            f"{selector!r} in {heading!r} at {page.url} scrolls horizontally, "
            "so the screenshot would cut it off; drop columns or widen the "
            "viewport."
        )
    return Image.open(BytesIO(await element.screenshot()))


async def capture_live(storage_state: Path) -> dict[str, list[list[Image.Image]]]:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            storage_state=storage_state,
            viewport={"width": VIEWPORT_WIDTH, "height": 1000},
            device_scale_factor=DEVICE_SCALE_FACTOR,
        )
        pages: dict[str, Page] = {}
        panels: dict[str, list[list[Image.Image]]] = {}
        for label, rows in LIVE_PANELS.items():
            panels[label] = []
            for cards in rows:
                row = []
                for card in cards:
                    path = card[0]
                    if path not in pages:
                        page = await context.new_page()
                        await page.goto(DASHBOARD_URL + path, wait_until="networkidle")
                        # The dashboard is a client-side app: wait for its
                        # charts and their entry animations.
                        await page.locator("main svg").first.wait_for()
                        await page.wait_for_timeout(2000)
                        pages[path] = page
                    row.append(await capture_card(pages[path], card))
                panels[label].append(row)
        await browser.close()
    return panels


async def save_login_state(storage_state: Path) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(DASHBOARD_URL)
        await asyncio.to_thread(
            input,
            "Log in with ORCID in the browser window, check a project page "
            "shows its repositories, then press Enter here... ",
        )
        await context.storage_state(path=storage_state)
        await browser.close()
    click.echo(f"Saved login session to {storage_state} (do not commit it).")


@click.group()
def cli() -> None:
    """Build Figure 2 from the CFDE ICC metrics dashboard."""


@cli.command("from-screenshot")
@click.option(
    "--screenshot",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=HERE / "dashboard_screenshot.png",
    show_default=True,
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    default=HERE / "figure2_dashboard.png",
    show_default=True,
)
@click.option("--width-cm", type=float, default=7.6, show_default=True)
def from_screenshot(screenshot: Path, output: Path, width_cm: float) -> None:
    """Restack the panels of the March 2026 three-column screenshot."""
    source = Image.open(screenshot).convert("RGB")
    panels = {
        label: [[source.crop(box) for box in row] for row in rows]
        for label, rows in SCREENSHOT_PANELS.items()
    }
    compose(panels, width_cm, output)


@cli.command()
@click.option(
    "--storage-state",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Logged-in Playwright session saved by the `login` command.",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    default=HERE / "figure2_dashboard.png",
    show_default=True,
)
@click.option("--width-cm", type=float, default=12.7, show_default=True)
def capture(storage_state: Path, output: Path, width_cm: float) -> None:
    """Re-capture a curated subset of the live dashboard."""
    panels = asyncio.run(capture_live(storage_state))
    compose(panels, width_cm, output)
    click.echo(
        f"Captured {datetime.date.today():%d %B %Y}: update the date in the "
        "Figure 2 legend to match."
    )


@cli.command()
@click.option(
    "--storage-state",
    type=click.Path(dir_okay=False, path_type=Path),
    default=HERE / ".dashboard-auth.json",
    show_default=True,
)
def login(storage_state: Path) -> None:
    """Open a browser to log in with ORCID and save the session for `capture`."""
    asyncio.run(save_login_state(storage_state))


if __name__ == "__main__":
    cli()
