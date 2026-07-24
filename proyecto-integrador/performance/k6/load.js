import http from "k6/http";
import { check, sleep } from "k6";

/**
 * Load moderno (k6 1.x): scenarios + ramping-vus + thresholds.
 * Misma "historia" que el smoke (health + product), con más VUs.
 * Si p95 / error rate / checks se rompen, K6 sale con código ≠ 0 (gate CI).
 */
export const options = {
  scenarios: {
    average_load: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "10s", target: 5 },
        { duration: "20s", target: 10 },
        { duration: "10s", target: 0 },
      ],
      gracefulRampDown: "10s",
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<800"],
    checks: ["rate>0.99"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://target:8080";

export default function () {
  const health = http.get(`${BASE_URL}/api/health`, {
    tags: { endpoint: "health" },
  });
  check(health, {
    "health status 200": (r) => r.status === 200,
  });

  const product = http.get(`${BASE_URL}/api/product`, {
    tags: { endpoint: "product" },
  });
  check(product, {
    "product status 200": (r) => r.status === 200,
    "product has title": (r) => String(r.body).includes("title"),
  });

  // Think time: un usuario real no dispara requests en bucle sin pausa.
  sleep(0.3);
}
