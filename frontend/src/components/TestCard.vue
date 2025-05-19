<template>
  <Card class="border-1 border-300 shadow-3 zoomin lg:max-w-30rem w-full h-full" :class="cardClasses">
    <template #title>
      <div>
        {{ test.name }}
        <div class="flex justify-content-end gap-2 mt-2">
          <Button class="px-2" v-if="showLink" size="small" @click="$router.push('/test/'+test._id)" outlined
                  label="Пройти"/>
          <Button v-if="test.username == user.username" size="small" outlined
                  @click="$router.push('/test/'+test._id+'/edit')" icon="pi pi-pencil" severity="warning"/>
        </div>
      </div>
    </template>
    <template #content>
      <div class="flex flex-column gap-3 justify-content-between">
        <div class="flex flex-column gap-2">
          <div v-if="test.description" class="mb-3">{{ test.description }}</div>
          <div v-if="showUser"><i class="pi pi-user"/> {{ test.username }}</div>
          <div v-if="test.completionTimeMinutes > 0">Время прохождения: <i
              class="pi pi-stopwatch mr-1"></i>{{ test.completionTimeMinutes }} минут
          </div>
          <div v-else>Время на прохождение теста неограниченно</div>
          <div v-if="test.timeoutMinutes > 0">Время для повторной попытки теста: <i
              class="pi pi-stopwatch mr-1"></i>{{ test.timeoutMinutes }} минут
          </div>
        </div>
        <div>
          <Tag @click="$emit('tagClick', tag)" v-for="tag in test.tags" :value="tag"
               class="shadow-2 mr-2 cursor-pointer hover:bg-primary-600"/>
        </div>
        <div class="my-2 w-full">
          <Button v-if="!openTestTimes?.finishedTime && timeToExpire" severity="warning" outlined class="text-sm w-full flex-column">
            <span>Вы не закончили проходить тест</span>
            <span>осталось: {{ timeToExpire }}</span>
          </Button>
          <Button v-else-if="timeToNextTry" severity="info" outlined class="text-sm w-full flex-column">
            <span>Повторно можно будет пройти через: {{ timeToNextTry }}</span>
          </Button>
        </div>
      </div>
    </template>
  </Card>
</template>

<script lang="ts">
import {PropType} from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import Tag from "primevue/tag";

import {TestAbout} from "@/questions"
import {mapState} from "vuex";
import {UserOpenedQuestionTimes} from "@/userOpenedQuestions";

export default {
  name: "TestCard",
  components: {Button, Card, Tag,},
  emits: ["tagClick"],
  props: {
    test: {required: true, type: TestAbout},
    openTestTimes: {required: false, type: Object as PropType<UserOpenedQuestionTimes> | undefined},
    showLink: {required: false, type: Boolean, default: true},
    showUser: {required: false, type: Boolean, default: true},
  },

  data() {
    return {
      timeToExpire: "",
      timeToNextTry: "",
    }
  },

  mounted() {
    this.getTimeRemaining()
  },

  computed: {
    ...mapState({
      user: (state: any) => state.auth.user,
    }),

    cardClasses() {
      if (this.timeToExpire) {
        return ["border-2", "border-orange-300"]
      }
      if (this.timeToNextTry) {
        return ["border-2", "border-blue-500"]
      }
    },
  },
  methods: {
    formatTime(ms: number): string {
      const totalSeconds = Math.floor(ms / 1000);
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      return `${minutes} мин. ${seconds < 10 ? '0' : ''}${seconds} сек.`;
    },

    getTimeRemaining(): void {
      if (!this.openTestTimes) return
      const now = new Date().getTime();
      const expireTime = new Date(this.openTestTimes.expireTime).getTime();
      const nextTryTime = new Date(this.openTestTimes.nextTryTime).getTime();

      const timeToExpire = expireTime - now;
      const timeToNextTry = nextTryTime - now;

      if (timeToExpire > 0) {
        this.timeToExpire = this.formatTime(timeToExpire)
        this.timeToNextTry = this.formatTime(timeToNextTry)
      } else {
        this.timeToExpire = ""
        this.timeToNextTry = this.formatTime(timeToNextTry)
      }
      setTimeout(this.getTimeRemaining, 1000)
    }
  }
}
</script>

<style scoped>

</style>