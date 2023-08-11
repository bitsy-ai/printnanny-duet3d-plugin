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
    ...mapState('settings', ['plugins'])
  },
  watch: {
    // connectDialogShown(to) { this.shown = to; },
    // lastHostname(to) {
    //     // Update the hostname
    //     this.hostname = to;
    // }
  },
  mounted() {
    this.clientId = this.plugins.PrintNannyDuetPlugin && this.plugins.PrintNannyDuetPlugin.clientId ? this.plugins.PrintNannyDuetPlugin.clientId : '';
    this.clientSecret = this.plugins.PrintNannyDuetPlugin && this.plugins.PrintNannyDuetPlugin.clientSecret ? this.plugins.PrintNannyDuetPlugin.clientSecret : '';
    this.apiUrl = this.plugins.PrintNannyDuetPlugin && this.plugins.PrintNannyDuetPlugin.apiUrl ? this.plugins.PrintNannyDuetPlugin.apiUrl : '';
  },
  methods: {
    ...mapMutations('settings', ['update']),
    submit() {
      console.log("this.$refs.form.validate()", this.$refs.form.validate());
      if (this.$refs.form.validate()) {
        const result = this.update({ plugins: { PrintNannyDuetPlugin: { clientId: this.clientId, clientSecret: this.clientSecret, apiUrl: this.apiUrl } } });
        console.log("Mutation result", result)
      }
    },
  },
};
</script>
