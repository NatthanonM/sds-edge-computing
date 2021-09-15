import axios from "axios";
import config from "../config/config";
import querysrc from "../data/query.json";

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
const queryService = {
  indoorQuery(arch, qId) {
    // MockTest
    // return new Promise((resolve, reject) => {
    //   resolve({
    //     location: { building: "A", floor: "1", tag: "21" },
    //     responseTime: 235.5,
    //   });
    // });
    if (arch === "A") {
      return cloudApi.post("", querysrc[qId]);
    }
    if (arch === "B") {
      return edgeApi.post("", querysrc[qId]);
    }
    return new Promise((resolve, reject) => {
      reject(new Error("wrong arguement"));
    });
  },
};
export default queryService;
