class SMCL {
    async init() {
      this.api = pywebview.api;
      await this.api.init_cmcl();
    }
    start() {
      $(window).on("pywebviewready", () => {
        this.init();
      });
    }
}

new SMCL().start();