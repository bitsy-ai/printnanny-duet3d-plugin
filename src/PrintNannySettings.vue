<template>
  <v-row>
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title class="headline"> Application Key </v-card-title>

        <v-card-text v-if="!credentialFile">
          Upload the JSON file you downloaded when creating a PrintNanny
          application key.
        </v-card-text>

        <v-card-text v-else> Using credentials file: {{}} </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <upload-btn
            ref="mainUpload"
            class="hidden-sm-and-down"
            :elevation="1"
            :directory="directory"
            :target="uploadTarget"
            color="primary"
            @upload-complete="onUploadComplete"
          >
            <v-icon class="mr-2">mdi-cloud-upload</v-icon>Upload application key
            & test connection
          </upload-btn>
          <v-btn v-if="credentialFile" color="green">Test Connection</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
"use strict";
import { mapState, mapMutations, mapGetters } from "vuex";
// import { logGlobal } from "@/utils/logging";
import Path from "@/utils/path";

export default {
  data() {
    return {
      credentialFile: null,
      directory: `${Path.system}/PrintNannyDuetPlugin/`,
    };
  },
  computed: {
    ...mapState("machine/model", {
      systemDirectory: (state) => state.directories.systemDirectory,
    }),
    ...mapState("settings", ["plugins"]),
    ...mapGetters("machine", ["connector"]),
  },
  mounted() {
    this.credentialFile =
      this.plugins.PrintNannyDuetPlugin &&
      this.plugins.PrintNannyDuetPlugin.credentialFile
        ? this.plugins.PrintNannyDuetPlugin.credentialFile
        : null;
  },
  methods: {
    ...mapMutations("settings", ["update"]),
    async onUploadComplete(files) {
      console.log("Finished uploading file", files);
      this.update({
        plugins: {
          PrintNannyDuetPlugin: {
            credentialFile: files,
          },
        },
      });
      await this.testConnection();
    },
    async testConnection() {
      const response = await this.connector.request(
        "GET",
        "machine/printnanny/connection-status",
        null,
        "json",
      );
      console.log("Connection status response: ", response);
    },
  },
};
</script>
