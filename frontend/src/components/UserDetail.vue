<template>
  <div class="mt-5 flex align-items-center m-2">
    <img :src="'https://ui-avatars.com/api/?size=32&name='+user.username+'&font-size=0.33&background=random&rounded=true'" height="64" class="mr-3" :alt="user.username">
    <div style="font-size: 2rem" class="mr-2">{{user.username}}</div>
    <div v-if="showLink">
      <Button label="Аккаунт" size="small" link @click="$router.push('/account/'+user.username)"/>
    </div>
  </div>

  <div class="my-3 text-500 flex flex-row flex-wrap">
    <div v-if="user.email" class="mx-2 flex align-items-center my-2">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="mr-2" viewBox="0 0 16 16">
        <path d="M2 2a2 2 0 0 0-2 2v8.01A2 2 0 0 0 2 14h5.5a.5.5 0 0 0 0-1H2a1 1 0 0 1-.966-.741l5.64-3.471L8 9.583l7-4.2V8.5a.5.5 0 0 0 1 0V4a2 2 0 0 0-2-2zm3.708 6.208L1 11.105V5.383zM1 4.217V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v.217l-7 4.2z"/>
        <path d="M14.247 14.269c1.01 0 1.587-.857 1.587-2.025v-.21C15.834 10.43 14.64 9 12.52 9h-.035C10.42 9 9 10.36 9 12.432v.214C9 14.82 10.438 16 12.358 16h.044c.594 0 1.018-.074 1.237-.175v-.73c-.245.11-.673.18-1.18.18h-.044c-1.334 0-2.571-.788-2.571-2.655v-.157c0-1.657 1.058-2.724 2.64-2.724h.04c1.535 0 2.484 1.05 2.484 2.326v.118c0 .975-.324 1.39-.639 1.39-.232 0-.41-.148-.41-.42v-2.19h-.906v.569h-.03c-.084-.298-.368-.63-.954-.63-.778 0-1.259.555-1.259 1.4v.528c0 .892.49 1.434 1.26 1.434.471 0 .896-.227 1.014-.643h.043c.118.42.617.648 1.12.648Zm-2.453-1.588v-.227c0-.546.227-.791.573-.791.297 0 .572.192.572.708v.367c0 .573-.253.744-.564.744-.354 0-.581-.215-.581-.8Z"/>
      </svg>
      Email: {{user.email}}
    </div>

    <div v-if="user.registrationDate" class="mx-2 flex align-items-center">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="mr-2" viewBox="0 0 16 16">
        <path d="M10.854 8.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L7.5 10.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
        <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M2 2a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"/>
        <path d="M2.5 4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5z"/>
      </svg>
      Зарегистрирован: {{formatDate(user.registrationDate)}}
    </div>
  </div>
</template>

<script lang="ts">
import Button from "primevue/button";
import {User} from "@/user";

export default {
  name: "UserDetail",
  components: {
    Button,
  },

  props: {
    user: {required: true, type: User},
    showLink: {required: false, type: Boolean, default: false},
  },

  methods: {
    formatDate(date: string): string {
      let d = new Date(date)
      return new Intl.DateTimeFormat("ru", {day: "numeric", month: "long", year: "numeric", hour: "numeric", minute: "numeric"}).format(d)
    },
  },

}
</script>

<style scoped>

</style>