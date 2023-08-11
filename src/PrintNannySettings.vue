<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-form ref="form" @submit.prevent="submit">
            <v-card-title class="headline"> PrintNanny Settings </v-card-title>

            <v-card-text>
              Copy/paste your printer's client id and client secret below.

              <v-text-field v-model="clientId" required label="Client ID"></v-text-field>
              <v-text-field v-model="clientSecret" type="password" required label="Client Secret"></v-text-field>
              <v-text-field v-model="apiUrl" required label="URL"></v-text-field>

            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text type="submit">Save</v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
"use strict";
import { mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      clientId: "",
      clientSecret: "",
      apiUrl: "https://v2.printnanny.ai"
    };
  },
  computed: {
    ...mapState('settings')
  },
  watch: {
    // connectDialogShown(to) { this.shown = to; },
    // lastHostname(to) {
    //     // Update the hostname
    //     this.hostname = to;
    // }
  },
  mounted() {
    this.clientId = this.settings.plugins.PrintNannyDuetPlugin && this.settings.plugins.PrintNannyDuetPlugin.clientId ? this.settings.plugins.PrintNannyDuetPlugin.clientId : '';
    this.clientSecret = this.settings.plugins.PrintNannyDuetPlugin && this.settings.plugins.PrintNannyDuetPlugin.clientSecret ? this.settings.plugins.PrintNannyDuetPlugin.clientSecret : '';
    this.apiUrl = this.settings.plugins.PrintNannyDuetPlugin && this.settings.plugins.PrintNannyDuetPlugin.apiUrl ? this.settings.plugins.PrintNannyDuetPlugin.apiUrl : '';
  },
  methods: {
    ...mapMutations('settings', ['update']),
    async submit() {
      if (this.$refs.form.validate()) {
        this.update(this.settings, { plugins: { PrintNannyDuetPlugin: { clientId: this.clientId, clientSecret: this.clientSecret, apiUrl: this.apiUrl } } })
      }
    },
  },
};
</script>
