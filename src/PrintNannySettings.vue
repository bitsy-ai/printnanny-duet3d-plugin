<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-form ref="form" @submit.prevent="submit">
            <v-card-title class="headline"> Application Key </v-card-title>

            <v-card-text>
              Upload the JSON file you downloaded when creating a PrintNanny
              application key.
              <v-text-field
                v-model="clientId"
                required
                label="Client ID"
              ></v-text-field>
              <v-text-field
                v-model="clientSecret"
                type="password"
                required
                label="Client Secret"
              ></v-text-field>
              <v-text-field
                v-model="apiUrl"
                required
                label="URL"
              ></v-text-field>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" type="submit" @click="submit"
                >Save & Test Connection</v-btn
              >
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
"use strict";
import { mapState, mapMutations, mapGetters } from "vuex";
// import { logGlobal } from "@/utils/logging";

export default {
  data() {
    return {
      clientId: "",
      clientSecret: "",
      apiUrl: "https://v2.printnanny.ai",
    };
  },
  computed: {
    ...mapState("settings", ["plugins"]),
    ...mapGetters('machine', ['connector']),
  },
  mounted() {
    this.clientId =
      this.plugins.PrintNannyDuetPlugin &&
      this.plugins.PrintNannyDuetPlugin.client_id
        ? this.plugins.PrintNannyDuetPlugin.client_id
        : "";
    this.clientSecret =
      this.plugins.PrintNannyDuetPlugin &&
      this.plugins.PrintNannyDuetPlugin.client_secret
        ? this.plugins.PrintNannyDuetPlugin.client_secret
        : "";
    this.apiUrl =
      this.plugins.PrintNannyDuetPlugin &&
      this.plugins.PrintNannyDuetPlugin.api_url
        ? this.plugins.PrintNannyDuetPlugin.api_url
        : "";
  },
  methods: {
    ...mapMutations("settings", ["update"]),
    async submit() {
      if (this.$refs.form.validate()) {
        this.update({
          plugins: {
            PrintNannyDuetPlugin: {
              client_id: this.clientId,
              client_secret: this.clientSecret,
              api_url: this.apiUrl,
            },
          },
        });
        await this.testConnection();
      }
    },
    async testConnection() {
      const response = await this.connector.request('GET', 'machine/printnanny/connection-status', null, 'json');
      console.log("Connection status response: ", response);
    },
  },
};
</script>
