class SMCL {
    constructor() {
      this.api = new API();

    }

    async initApi() {
      await this.api.init();
      this.api.log('初始化完毕');
    }

    async init() {
      await this.initApi();
      await this.setBackground();
    }
    start() {
      $(window).on("pywebviewready", () => {
        this.init();
      });
    }
}

new SMCL().start();