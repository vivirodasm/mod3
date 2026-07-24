import http from "k6/http";
import { check, sleep } from "k6";

/**
 * Smoke de performance — pocos VUs, debe pasar siempre contra el target local.
 * Checks = asserts por request. Thresholds = criterio de gate (exit code).
 * BASE_URL por defecto: http://target:8080 (red Docker Compose).
 */
export const options = {
  vus: 2,
  duration: "15s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
    checks: ["rate>0.99"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://target:8080";

export default function () {
  const health = http.get(`${BASE_URL}/api/health`);
  check(health, {
    "health status 200": (r) => r.status === 200,
    "health body ok": (r) =>
      String(r.body).includes('"status": "ok"') ||
      String(r.body).includes('"status":"ok"'),
  });

  const product = http.get(`${BASE_URL}/api/product`);
  check(product, {
    "product status 200": (r) => r.status === 200,
    "product has title": (r) => String(r.body).includes("title"),
  });

  sleep(0.5);
}
