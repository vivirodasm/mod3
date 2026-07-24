import http from "k6/http";
import { check, sleep } from "k6";

/**
 * Demo de gate ROJO: threshold imposible (p95 < 1ms) contra latencia real.
 * Úsalo en clase para mostrar "performance falla → no merge".
 */
export const options = {
  vus: 2,
  duration: "10s",
  thresholds: {
    http_req_duration: ["p(95)<1"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://target:8080";

export default function () {
  const res = http.get(`${BASE_URL}/api/health`);
  check(res, { "status 200": (r) => r.status === 200 });
  sleep(0.2);
}
