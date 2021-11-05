import axios from "axios";
import config from "../config/config";
import querysrc from "../data/query.json";
import fp1 from "../data/fp1.json";
import fp2 from "../data/fp2.json";
import fp3 from "../data/fp3.json";
import fp4 from "../data/fp4.json";
import fp5 from "../data/fp5.json";
import fp6 from "../data/fp6.json";
import fp7 from "../data/fp7.json";
import fp8 from "../data/fp8.json";
import fp9 from "../data/fp9.json";
import fp10 from "../data/fp10.json";

const fps = [
  { b_id: "POL3", fp: fp1 },
  { b_id: "EN100", fp: fp2 },
  { b_id: "POL3", fp: fp3 },
  { b_id: "ARCH", fp: fp4 },
  { b_id: "ENG4", fp: fp5 },
  { b_id: "ENG2", fp: fp6 },
  { b_id: "EN100", fp: fp7 },
  { b_id: "ENG2", fp: fp8 },
  { b_id: "ENG1", fp: fp9 },
  { b_id: "ENG1", fp: fp10 },
];

const edgeApi = axios.create({
  baseURL: `${config.edge_url}/`,
  headers: {
    "Content-Type": "application/json",
  },
});
const cloudApi = axios.create({
  baseURL: `${config.cloud_url}/`,
  headers: {
    "Content-Type": "application/json",
  },
});

edgeApi.interceptors.request.use((x) => {
  x.meta = x.meta || {};
  x.meta.requestStartedAt = new Date().getTime();
  return x;
});
edgeApi.interceptors.response.use(
  (x) => {
    x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt;
    return x;
  },
  (err) => {
    throw err;
  }
);

cloudApi.interceptors.request.use((x) => {
  x.meta = x.meta || {};
  x.meta.requestStartedAt = new Date().getTime();
  return x;
});
cloudApi.interceptors.response.use(
  (x) => {
    x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt;
    return x;
  },
  (err) => {
    throw err;
  }
);
const queryService = {
  indoorQuery(arch, qId) {
    // MockTest;
    // return new Promise((resolve, reject) => {
    //   setTimeout(
    //     () =>
    //       resolve({
    //         data: { building: "A", floor: "1", tag: "21" },
    //         responseTime: 235.5,
    //       }),
    //     1000
    //   );
    // });
    if (arch === "A") {
      return cloudApi.post("/get-location", {
        building_id: fps[qId - 1].b_id,
        finger_print: fps[qId - 1].fp,
      });
    }
    if (arch === "B") {
      return edgeApi.post("/get-location", {
        building_id: fps[qId - 1].b_id,
        finger_print: fps[qId - 1].fp,
      });
    }
    return new Promise((resolve, reject) => {
      reject(new Error("wrong arguement"));
    });
  },
};
export default queryService;
