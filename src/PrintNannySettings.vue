<template>
  <v-dialog v-model="shown" persistent no-click-animation width="360">
    <v-card>
      <v-form ref="form" @submit.prevent="submit">
        <v-card-title class="headline"> PrintNanny Settings </v-card-title>

        <v-card-text>
          Copy/paste your printer's client id and client secret below.

          <v-text-field v-model="clientId" required></v-text-field>
          <v-text-field
            v-model="clientSecret"
            type="password"
            required
          ></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text type="submit">Save</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
"use strict";

// import { mapState, mapActions, mapMutations } from "vuex";
export default {
  data() {
    return {
      shown: false,
      clientId: "",
      clientSecret: "",
    };
  },
  computed: {
    // ...mapState('plugins', ['PrintNannyDuetPlugin'])
  },
  watch: {
    // connectDialogShown(to) { this.shown = to; },
    // lastHostname(to) {
    //     // Update the hostname
    //     this.hostname = to;
    // }
  },
  mounted() {
    // this.hostname = this.passwordRequired ? location.host : this.lastHostname;
    // this.shown = this.connectDialogShown;
  },
  methods: {
    // ...mapMutations(['showConnectDialog', 'hideConnectDialog']),
    async submit() {
      // if (this.shown && this.$refs.form.validate()) {
      //     this.hideConnectDialog();
      //     try {
      //         await this.connect({ hostname: this.hostname, password: this.password });
      //         this.password = '';
      //     } catch (e) {
      //         console.warn(e);
      //         this.showConnectDialog();
      //     }
      // }
    },
  },
};
</script>
