import Vue from "vue";
import { registerRoute } from "../../routes";
import PrintNannySettings from "./PrintNannySettings.vue";
import CustomUploadBtn from "./CustomUploadBtn.vue";

registerRoute(PrintNannySettings, {
  Settings: {
    PrintNannySetting: {
      icon: "mdi-crystal-ball",
      caption: "PrintNanny",
      path: "/printnanny",
    },
  },
});

Vue.component("CustomUploadBtn", CustomUploadBtn);
