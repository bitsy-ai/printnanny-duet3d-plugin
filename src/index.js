import { registerRoute } from "../../routes";
import PrintNannySettings from "./PrintNannySettings.vue";

registerRoute(PrintNannySettings, {
  Settings: {
    PrintNannySetting: {
      icon: "mdi-crystal-ball",
      caption: "PrintNanny",
      path: "/printnanny",
    },
  },
});
