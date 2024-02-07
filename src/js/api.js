class API {
    async init() {
      this.debug = await this.isDebug();
    }
    print(msg) {
      pywebview.api.log(msg);
    }
    async isDebug() {
      return await pywebview.api.isDebug();
    }
    log(msg) {
      if (!this.debug) return;
      const timeStr = new Date().toLocaleTimeString();
      this.print(`[SMCL] [${timeStr}] ${msg}`);
    }
    async cmcl(cmd) {
      return await pywebview.api.cmcl(cmd);
    }
    async get(url) {
      this.log(`GET请求: ${url}`);
      return await pywebview.api.get(url);
    }
}