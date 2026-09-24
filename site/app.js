const picker = document.querySelector("#genre");
const status = document.querySelector("#status");
const chart = document.querySelector("#chart");
const drawing = document.querySelector("#drawing");
const caption = document.querySelector("#caption");
const title = document.querySelector("#chart-title");

const TOP = 15;
let games = [];

function eligible(records) {
  return records.filter(game =>
    game.visible === 1 &&
    game.rollupMode !== "series" &&
    Number(game.hours) > 0
  );
}

function genresByHours(records) {
  const totals = new Map();
  for (const game of records) {
    for (const genre of game.genres || []) {
      totals.set(genre, (totals.get(genre) || 0) + game.hours);
    }
  }
  return [...totals.entries()].sort((a, b) => b[1] - a[1]);
}

function gamesForGenre(genre) {
  return games
    .filter(game => (game.genres || []).includes(genre))
    .sort((a, b) => b.hours - a.hours);
}

function svg(tag, attributes, text = "") {
  const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value);
  node.textContent = text;
  drawing.append(node);
  return node;
}

function drawGenre() {
  const genre = picker.value;
  const matches = gamesForGenre(genre);
  const total = matches.reduce((sum, game) => sum + game.hours, 0);
  const shown = matches.slice(0, TOP).reverse();
  const maximum = Math.max(...shown.map(game => game.hours));
  const left = 260;
  const width = 560;
  const row = 28;
  const top = 65;
  const height = Math.max(170, top + shown.length * row + 65);

  drawing.replaceChildren();
  chart.setAttribute("viewBox", `0 0 900 ${height}`);
  for (const percent of [0, .5, 1]) {
    const x = left + width * percent;
    svg("line", { x1: x, x2: x, y1: 36, y2: height - 38, stroke: "#e8e4de" });
    svg("text", { x, y: height - 16, "text-anchor": "middle", "font-size": 13, fill: "#6f6a64" },
        `${Math.round(maximum * percent)}h`);
  }

  for (const [index, game] of shown.entries()) {
    const y = top + index * row;
    const barWidth = game.hours / maximum * width;
    svg("text", { x: left - 12, y: y + 15, "text-anchor": "end", "font-size": 14, fill: "#1a1a1a" }, game.titleEn);
    svg("rect", { x: left, y, width: barWidth, height: 18, rx: 2, fill: "#d6591d" });
    svg("text", { x: left + barWidth + 7, y: y + 15, "font-size": 13, fill: "#1a1a1a" }, `${game.hours}h`);
  }

  const extra = matches.length - shown.length;
  const summary = `${genre}: ${matches.length} games · ${total.toLocaleString()} associated hours`;
  status.textContent = summary;
  caption.textContent = extra > 0
    ? `Showing the ${TOP} longest of ${matches.length} games. ${extra} shorter games are not drawn.`
    : `Showing all ${matches.length} matching games.`;
  title.textContent = `Games and recorded hours associated with ${genre}`;
  chart.removeAttribute("hidden");
}

async function loadGames() {
  try {
    const response = await fetch("../data/games.generated.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    games = eligible(data.games || []);
    const genres = genresByHours(games);
    if (!genres.length) throw new Error("No genre records found");
    for (const [genre, hours] of genres) picker.add(new Option(`${genre} (${hours.toLocaleString()}h)`, genre));
    picker.disabled = false;
    picker.addEventListener("change", drawGenre);
    drawGenre();
  } catch (error) {
    status.textContent = `Could not load the game records: ${error.message}. Serve this folder over HTTP, not file://.`;
  }
}

loadGames();
