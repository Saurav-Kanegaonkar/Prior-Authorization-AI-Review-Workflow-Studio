import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import path from "node:path";

async function loadChromium() {
  try {
    const module = await import("playwright");
    return module.chromium;
  } catch {
    const moduleDir = process.env.PLAYWRIGHT_NODE_MODULES;
    if (!moduleDir) {
      throw new Error("Install Playwright or set PLAYWRIGHT_NODE_MODULES to a node_modules directory that contains Playwright.");
    }
    const require = createRequire(path.join(moduleDir, "playwright/package.json"));
    return require("playwright").chromium;
  }
}

const baseUrl = process.env.APP_URL || "http://127.0.0.1:4180";
const imageDir = path.resolve("docs/images");

const shots = [
  { tab: "Pipeline", file: "pipeline-command-center.png" },
  { tab: "Thresholds", file: "threshold-studio.png" },
  { tab: "Clinical QA", file: "clinical-qa-workbench.png" },
  { tab: "Feedback", file: "feedback-compliance-loop.png" },
];

await mkdir(imageDir, { recursive: true });

const chromium = await loadChromium();
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });

const consoleErrors = [];
page.on("console", (message) => {
  if (message.type() === "error") consoleErrors.push(message.text());
});

await page.goto(baseUrl, { waitUntil: "networkidle" });
await page.locator("h1").waitFor();

for (const shot of shots) {
  await page.getByRole("button", { name: shot.tab }).click();
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(imageDir, shot.file), fullPage: false });
}

await page.setViewportSize({ width: 390, height: 860 });
await page.goto(baseUrl, { waitUntil: "networkidle" });
await page.locator("h1").waitFor();
const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);

await browser.close();

if (consoleErrors.length) {
  throw new Error(`Console errors: ${consoleErrors.join(" | ")}`);
}
if (mobileOverflow) {
  throw new Error("Mobile viewport has horizontal overflow.");
}

console.log("Captured screenshots and verified mobile layout.");
