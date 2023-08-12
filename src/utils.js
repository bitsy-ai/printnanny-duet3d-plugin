import * as api from "printnanny-factory-rest-api";
import { logGlobal } from "@/utils/logging";

async function getJwt(clientId, clientSecret, apiUrl) {
  const req = { grant_type: "client_credentials" };
  let apiconfig = new api.Configuration({
    basePath: apiUrl,
  });
  const res = await api.AuthApiFactory(apiconfig, apiUrl).oTokenCreate(req);
  if (res && res.data && res.data.access_token && res.data.refresh_token) {
    return res.data;
  } else {
    logGlobal("error", "[PrintNanny] Failed to authenticate", res.data);
  }
}

export { getJwt };
