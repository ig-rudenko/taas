<template>
  <span @click="showChangePasswordModal=true" class="cursor-pointer">Сменить пароль</span>
  <Dialog v-model:visible="showChangePasswordModal" modal header="Смена пароля" >
    <div class="flex flex-column gap-2 m-2">
      <label for="password1">Введите новый пароль</label>
      <Password id="password1" v-model="newPasswords.password1"/>
    </div>
    <div class="flex flex-column gap-2 m-2">
      <label for="password2">Подтвердите</label>
      <InputText type="password" id="password2" v-model="newPasswords.password2"/>
    </div>
    <div class="m-2">
      <span v-if="newPasswords.password1 !== newPasswords.password2">Пароли не совпадают</span>
      <span v-else-if="newPasswords.password1.length < 8">Укажите более 8 символов</span>
      <Button v-if="newPasswords.valid" @click="changePassword" class="mt-2" size="small">Обновить</Button>
    </div>
  </Dialog>
</template>

<script lang="ts">
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Password from "primevue/password";

import api from "@/services/api";
import {ChangePassword} from "@/user";

export default {
  name: "ChangePasswordForm",
  components: {
    Button,
    Dialog,
    InputText,
    Password,
  },
  emits: ["error", "change"],

  data() {
    return {
      showChangePasswordModal: false,
      newPasswords: new ChangePassword()
    }
  },

  methods: {
    changePassword() {
      if (!this.newPasswords.valid) return;

      api.patch("users/myself/password", {password: this.newPasswords.password1}).then(
          () => this.$emit("change"),
          (e: any) => this.$emit("error", e)
      )
    }
  }
}
</script>

<style scoped>

</style>