<template>
  <v-card>
    <v-form ref="form" @submit.prevent="submit">
      <v-card-title class="headline"> Application Key </v-card-title>

      <v-card-text>
        Upload the JSON file you downloaded when creating a PrintNanny
        application key.

        <upload-btn
          target="system"
          color="primary"
          directory="/opt/dsf/plugins/PrintNannyDuetPlugin/"
        ></upload-btn>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="indigo darken-1" @click="testConnection"
          >Test Connection</v-btn
        >
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
"use strict";
import { mapState, mapMutations } from "vuex";
import UploadBtn from "@/components/buttons/UploadBtn.vue";
// import * as api from "printnanny-factory-rest-api";
// import { logGlobal } from "@/utils/logging";
import { getJwt } from "@/utils";

export default {
  data() {
    return {
      error: undefined,
      printerId: "",
      aapplicationId: "",
      workspaceId: "",
      clientId: "",
      clientSecret: "",
      apiUrl: "https://v2.printnanny.ai",
    };
  },
  computed: {
    ...mapState("settings", ["plugins"]),
  },
  mounted() {
    this.clientId =
      this.plugins.PrintNannyDuetPlugin &&
      this.plugins.PrintNannyDuetPlugin.clientId
        ? this.plugins.PrintNannyDuetPlugin.clientId
        : "";
    this.clientSecret =
      this.plugins.PrintNannyDuetPlugin &&
      this.plugins.PrintNannyDuetPlugin.clientSecret
        ? this.plugins.PrintNannyDuetPlugin.clientSecret
        : "";
    this.apiUrl =
      this.plugins.PrintNannyDuetPlugin &&
      this.plugins.PrintNannyDuetPlugin.apiUrl
        ? this.plugins.PrintNannyDuetPlugin.apiUrl
        : "";
  },
  methods: {
    ...mapMutations("settings", ["update"]),
    submit() {
      if (this.$refs.form.validate()) {
        this.update({
          plugins: {
            PrintNannyDuetPlugin: {
              clientId: this.clientId,
              clientSecret: this.clientSecret,
              apiUrl: this.apiUrl,
            },
          },
        });
      }
    },
    testConnection() {
      const jwt = getJwt(this.clientId, this.clientSecret, this.apiUrl);
      console.log("Got JWT", jwt);
    },
  },
};
</script>
