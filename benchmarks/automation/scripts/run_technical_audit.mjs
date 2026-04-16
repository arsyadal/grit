#!/usr/bin/env node

import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import process from "node:process";
import lighthouse from "lighthouse";
import { launch as launchChrome } from "chrome-launcher";
import puppeteer from "puppeteer-core";
import axe from "axe-core";

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      continue;
    }
    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    index += 1;
  }
  return args;
}

function resolvePath(root, maybePath) {
  if (!maybePath) {
    return null;
  }
  if (path.isAbsolute(maybePath)) {
    return maybePath;
  }
  return path.resolve(root, maybePath);
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function writeJson(filePath, data) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(data, null, 2) + "\n", "utf8");
}

async function createSingleFileServer(renderPath) {
  const html = await fs.readFile(renderPath, "utf8");
  const server = http.createServer((req, res) => {
    if (!req.url || req.url === "/" || req.url.startsWith("/?")) {
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(html);
      return;
    }
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not found");
  });

  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  if (!address || typeof address === "string") {
    throw new Error("Unable to determine local audit server address.");
  }

  return {
    server,
    url: `http://127.0.0.1:${address.port}/`,
    close: async () => new Promise((resolve, reject) => server.close((error) => (error ? reject(error) : resolve()))),
  };
}

async function runLighthouseAudit(url, chromePath) {
  const chrome = await launchChrome({
    chromePath,
    chromeFlags: ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"],
  });

  try {
    const runnerResult = await lighthouse(
      url,
      {
        port: chrome.port,
        output: "json",
        logLevel: "error",
        onlyCategories: ["performance", "accessibility"],
        emulatedFormFactor: "desktop",
        screenEmulation: { disabled: true },
      },
      undefined,
    );

    return {
      performance: Math.round((runnerResult.lhr.categories.performance.score || 0) * 100),
      accessibility: Math.round((runnerResult.lhr.categories.accessibility.score || 0) * 100),
      report: runnerResult.report,
    };
  } finally {
    await chrome.kill();
  }
}

async function runAxeAudit(url, chromePath) {
  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 1200, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: "networkidle0" });
    await page.addScriptTag({ content: axe.source });
    const results = await page.evaluate(async () => {
      return await axe.run(document, {
        runOnly: {
          type: "tag",
          values: ["wcag2a", "wcag2aa"],
        },
      });
    });

    return {
      violations: results.violations.length,
      details: results.violations.map((violation) => ({
        id: violation.id,
        impact: violation.impact,
        help: violation.help,
        nodes: violation.nodes.length,
      })),
    };
  } finally {
    await browser.close();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const runArg = args.run;
  const condition = args.condition;
  if (!runArg || !condition) {
    throw new Error("Usage: node run_technical_audit.mjs --run <run-dir> --condition <baseline|grit> [--chrome-binary <path>]");
  }

  const runDir = path.resolve(runArg);
  const chromeBinary = args["chrome-binary"] || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  const outputArtifactPath = path.join(runDir, "outputs", `${condition}.json`);
  const metricsPath = path.join(runDir, "metrics", "technical.json");
  const outputArtifact = await readJson(outputArtifactPath);
  const metrics = await readJson(metricsPath);
  const renderTarget = resolvePath(runDir, outputArtifact.render_target_path || outputArtifact.code_path);
  if (!renderTarget) {
    throw new Error(`No render target defined for condition: ${condition}`);
  }

  const server = await createSingleFileServer(renderTarget);
  try {
    const lighthouseResult = await runLighthouseAudit(server.url, chromeBinary);
    const axeResult = await runAxeAudit(server.url, chromeBinary);

    metrics[condition].lighthouse_performance = lighthouseResult.performance;
    metrics[condition].lighthouse_accessibility = lighthouseResult.accessibility;
    metrics[condition].axe_violations = axeResult.violations;
    await writeJson(metricsPath, metrics);

    const auditDetailsPath = path.join(runDir, "metrics", `${condition}-audit.json`);
    await writeJson(auditDetailsPath, {
      condition,
      audited_url: server.url,
      render_target_path: renderTarget,
      lighthouse: {
        performance: lighthouseResult.performance,
        accessibility: lighthouseResult.accessibility,
      },
      axe: {
        violations: axeResult.violations,
        details: axeResult.details,
      },
    });

    process.stdout.write(JSON.stringify({
      condition,
      lighthouse_performance: lighthouseResult.performance,
      lighthouse_accessibility: lighthouseResult.accessibility,
      axe_violations: axeResult.violations,
      details_path: auditDetailsPath,
    }, null, 2));
    process.stdout.write("\n");
  } finally {
    await server.close();
  }
}

main().catch((error) => {
  process.stderr.write(String(error.stack || error) + "\n");
  process.exit(1);
});
