<template>
  <Card class="m-2 border-1 border-300 shadow-3 zoomin">
    <template #title>
      <div class="flex align-items-center">
        <span class="mr-3">{{test.name}}</span>
        <Button v-if="editLink" size="small" @click="$router.push('/test/'+test._id+'/edit')" link label="Редактировать"/>
        <Button v-else size="small" @click="$router.push('/test/'+test._id)" link label="Пройти"/>
      </div>
    </template>
    <template #content>
      <div class="m-0">
        <div v-if="test.description" class="mb-3">{{test.description}}</div>
        <div v-if="showUser"><i class="pi pi-user"/> {{test.username}}</div>
        <p v-if="test.completionTimeMinutes > 0">Время прохождения: <i class="pi pi-stopwatch mr-1"></i>{{test.completionTimeMinutes}} минут</p>
        <p v-else>Время на прохождение теста неограниченно</p>
        <p v-if="test.timeoutMinutes > 0">Время для повторной попытки теста: <i class="pi pi-stopwatch mr-1"></i>{{test.timeoutMinutes}} минут</p>
        <div>
          <Tag @click="$emit('tagClick', tag)" v-for="tag in test.tags" :value="tag" class="mr-2 cursor-pointer"/>
        </div>
      </div>
    </template>
  </Card>
</template>

<script lang="ts">
import Button from "primevue/button";
import Card from "primevue/card";
import Tag from "primevue/tag";

import {TestAbout} from "@/questions"

export default {
  name: "TestCard",
  components: {
    Button,
    Card,
    Tag,
  },
  emits: ["tagClick"],
  props: {
    test: {required: true, type: TestAbout},
    editLink: {required: false, type: Boolean, default: false},
    showUser: {required: false, type: Boolean, default: true},
  }
}
</script>

<style scoped>

</style>