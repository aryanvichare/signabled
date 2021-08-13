import axios from "axios";
import { server } from "../../config/server";

export default async function handler(req, res) {
  const { proxyRoute } = req.query;
  console.log(proxyRoute);

  const result = await axios.post(`${server}/${proxyRoute}`, req.body);
  res.json(result.data);
}
