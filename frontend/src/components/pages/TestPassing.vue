<template>
  <Menu/>
  <Toast/>

  <div v-if="testData" class="sticky top-0 p-3 p-card border-bottom-1 border-200 flex justify-content-between align-items-center" style="z-index: 999">
    <div class="flex flex-wrap">
      <div v-for="(question, qID) in testData.questions">
        <a :href="'#question-'+(qID+1)">
          <Button :label="String(qID+1)" raised rounded size="small"
                  :outlined="!isQuestionHasAnswer(question)"
                  :severity="questionCorrect(question)?'':'danger'" />
        </a>
      </div>
    </div>

    <div>
      <h2 v-if="secondsLeft !== 0 && !testFinished" :class="timerClasses">{{secondsLeftString}}</h2>
      <h2 v-if="timeIsUp && !testFinished" class="m-0 mr-3 bg-red-500 p-2 text-white border-round">Время вышло!</h2>
    </div>

  </div>

  <Container v-if="testData">


    <h2 class="my-5">{{testData.name}}</h2>
    <p>{{testData.description}}</p>

    <div v-for="(question, qID) in testData.questions" class="relative">
      <div :id="'question-'+(qID+1)" class="absolute" style="top: -100px"></div>

      <div class="relative p-5 my-5 border-round border-1 border-300 hover:shadow-2 p-card">

        <Badge size="xlarge" class="absolute question-number"
               :value="'# ' + (qID + 1)"
               :severity="questionCorrect(question)?'':'danger'" />


        <div class="my-2 md:font-normal" v-html="formatText(question.text)"></div>

        <div v-for="(answer, aID) in question.answers" :key="'q'+qID+'a'+aID">
          <div :class="answerClasses(answer)">
            <Checkbox class="mr-3" :disabled="testFinished" v-model="answer.isValid" :binary="true"/>
            <div class="cursor-pointer" @click="testFinished?null:answer.isValid=!answer.isValid" v-html="formatText(answer.text)"></div>
          </div>
        </div>

        <!-- Верный ответ -->
        <div v-if="question.explanation && testData.passedSuccessfully"
             v-html="formatText(question.explanation)"
             class="mt-3 p-3 border-1 border-200 border-round p-message-success p-message"></div>

      </div>
    </div>

    <div v-if="testFinished">
      <div v-if="testData.passedSuccessfully" class="text-center m-4">
        <i class="pi pi-star-fill mx-2 text-orange-400"/>
        Поздравляем
        <i class="pi pi-star-fill mx-2 text-orange-400"/>
        <div>Вы успешно прошли тест</div>
      </div>
      <div v-else class="text-center m-4">
        😞 Сожалеем 😞
        <div>Для прохождения теста необходимо набрать более 70% верных ответов, а у вас {{testData.percents}}%</div>
        <div>Не отчаивайтесь! Вы сможете пройти тест позднее 😊</div>
      </div>
      <div class="flex justify-content-center">
        <Knob v-model="testData.userScore" :value-color="testData.passedSuccessfully?'teal':'#ff6767'" readonly :max="testData.totalScore" :size="200"/>
      </div>
    </div>

    <div class="my-5 flex justify-content-center">
      <Button v-if="isAllQuestionsHasAnswer && !testFinished && !timeIsUp" label="Завершить тест" @click="submitTest" />
      <Button v-else-if="testFinished || timeIsUp" label="Вернуться к списку" @click="$router.push('/tests')" />
    </div>

  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script lang="ts">
import Badge from "primevue/badge";
import Button from "primevue/button";
import Checkbox from "primevue/checkbox";
import Knob from "primevue/knob";
import ScrollTop from "primevue/scrolltop";
import Toast from 'primevue/toast';

import {findCodeBlocksAndFormat} from "@/formatters.js"
import Container from "@/components/Container.vue";
import Menu from "@/components/Menu.vue";
import api from "@/services/api.js";
import Footer from "@/components/Footer.vue";
import {Answer, createNewTestForPassing, Question, TestForPassing} from "@/questions";

export default {
  name: "TestPassing",
  components: {
    Footer,
    Badge,
    Button,
    Checkbox,
    Container,
    Knob,
    Menu,
    ScrollTop,
    Toast,
  },

  data() {
    return {
      testData: null as TestForPassing,
      testFinished: false,
      timeIsUp: false,
      secondsLeft: 0,
    }
  },

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")

    api.get("questions/group/"+this.testID).then(
        res => {
          this.testData = createNewTestForPassing(res.data);
          this.startTimer();
        },
        error => this.handleError(error)
    )

  },

  computed: {
    testID(): string {
      return this.$route.params.id
    },
    loggedIn(): boolean {
      return this.$store.state.auth.status.loggedIn;
    },

    secondsLeftString(): string {
      if (this.secondsLeft === null) return "__:__"

      let minutes = Math.floor(this.secondsLeft / 60)
      let seconds = this.secondsLeft % 60

      let minStr = String(minutes)
      let secStr = String(seconds)
      if (minutes < 10) {
        minStr = "0" + minStr
      }
      if (seconds < 10) {
        secStr = "0" + secStr
      }
      return minStr + ":" + secStr
    },

    timerClasses(): Array<string> {
      let classes = ["m-0", "mr-3", "p-2", "border-round"]
      if (this.secondsLeft <= 60) {
        classes.push("bg-red-500", "text-white")
      }
      return classes
    },

    isAllQuestionsHasAnswer(): boolean {
      for (const question of this.testData.questions) {
        if (!this.isQuestionHasAnswer(question)) return false;
      }
      return true
    },

  },

  methods: {
    formatText(text: string): string {
      if (!text) return ""
      return findCodeBlocksAndFormat(text)
    },

    answerClasses(answer: Answer): Array<string> {
      if (answer.isCorrect) {
        return ["p-3", "flex", "flex-row"]
      } else {
        return ["p-3", "flex", "flex-row", "border-left-3", "border-red-600"]
      }
    },

    submitTest(): void {
      if (this.timeIsUp) {
        this.$toast.add({ severity: 'warn', summary: 'Упс', detail: "Время теста вышло!", life: 3000 });
      }
      api.post("questions/validate", this.testData).then(
          res => {
            this.testData = createNewTestForPassing(res.data);
            this.testFinished = true;
          },
          error => this.handleError(error)
      )
    },

    handleError(error: any): void {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      if (message.includes("Данный тест повторно вы сможете пройти")) {
        this.$toast.add({ severity: 'info', summary: 'Ожидание', detail: message, life: 3000 });
      } else {
        this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
      }
    },

    isQuestionHasAnswer(question: Question): boolean {
      for (const answer of question.answers) {
        if (answer.isValid) return true;
      }
      return false
    },

    questionCorrect(question: Question): boolean {
      for (const answer of question.answers) {
        if (!this.testFinished && !answer.isCorrect) return false;
        if (this.testFinished && answer.trueValid !== answer.isValid) return false;
      }
      return true
    },

    startTimer(): void {
      if (this.testData.completionTimeSeconds > 0) {
        this.secondsLeft = this.testData.completionTimeSeconds
        setTimeout(this.timer, 1000)
      } else if (this.testData.completionTimeSeconds === -1) {
        return
      }
    },

    timer(): void {
      if (this.testFinished) return;

      if (this.secondsLeft > 0) {
        this.secondsLeft--
        setTimeout(this.timer, 1000)
      } else {
        this.timeIsUp = true;
      }
    },

  }
}
</script>

<style scoped>
.question-number {
  top: -20px;
  right: -20px;
}

@media (width < 1111px) {
  .question-number {
    right: -1px;
  }
}
</style>

<style>
.token.operator,
.token.entity,
.token.url,
.language-css .token.string,
.style .token.string {
  background: none!important;
}

</style>