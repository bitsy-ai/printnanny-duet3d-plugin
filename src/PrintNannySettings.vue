<template>
  <v-row>
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title class="headline"> Application Key </v-card-title>

        <v-card-text v-if="!credentialFile">
          Upload the JSON file you downloaded when creating a PrintNanny
          application key.
        </v-card-text>

        <v-card-text v-else>
          Using credentials file: <strong>{{ credentialFile }} </strong>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <CustomUploadBtn
            v-if="!credentialFile"
            ref="mainUpload"
            :elevation="1"
            :directory="directory"
            :target="uploadTarget"
            color="primary"
            @upload-complete="onUploadComplete"
          >
            <v-icon class="mr-2">mdi-cloud-upload</v-icon>Upload application key
          </CustomUploadBtn>
          <CustomUploadBtn
            v-else
            ref="mainUpload"
            :elevation="1"
            :directory="directory"
            :target="uploadTarget"
            color="red"
            @upload-complete="onUploadComplete"
          >
            <v-icon class="mr-2">mdi-cloud-upload</v-icon>Overwrite application
            key
          </CustomUploadBtn>
          <v-btn v-if="credentialFile" color="secondary" @click="testConnection"
            >Test Connection</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
"use strict";
import { mapState, mapMutations, mapGetters } from "vuex";
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
    ...mapMutations("settings", ["setPluginData"]),
    async onUploadComplete(files) {
      console.log("Finished uploading file", files[0]);
      this.setPluginData({
        plugin: "PrintNannyDuetPlugin",
        key: "credentialFile",
        value: files[0].filename,
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
