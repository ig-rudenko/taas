<template>
  <Menu/>
  <Toast/>

  <div v-if="testData" class="sticky top-0 p-3 bg-white border-bottom-1 border-200" style="z-index: 999">
    <template v-for="(question, qID) in testData.questions">
      <a :href="'#question-'+(qID+1)">
        <Button :label="String(qID+1)" raised rounded size="small"
                :outlined="!isQuestionHasAnswer(question)"
                :severity="questionCorrect(question)?'':'danger'" />
      </a>
    </template>
  </div>

  <Container v-if="testData">


    <h2 class="m-5">{{testData.name}}</h2>

    <div v-for="(question, qID) in testData.questions" class="relative">
      <div :id="'question-'+(qID+1)" class="absolute" style="top: -100px"></div>

      <div class="relative p-5 my-5 border-round border-1 border-300 hover:shadow-2 hover:bg-primary-50">

        <Badge size="xlarge" class="absolute question-number"
               :value="'# ' + (qID + 1)"
               :severity="questionCorrect(question)?'':'danger'" />


        <div class="my-2 md:font-normal">{{question.text}}</div>

        <div v-for="(answer, aID) in question.answers" :key="'q'+qID+'a'+aID">
          <div :class="answerClasses(answer)">
            <Checkbox class="mr-3" :disabled="testFinished" :inputId="'q'+qID+'a'+aID" v-model="answer.is_valid" :binary="true"/>
            <label :for="'q'+qID+'a'+aID" class="cursor-pointer">{{formatText(answer.text)}}</label>
          </div>
        </div>

        <div v-if="question.explanation && isTestPassed" class="mt-3 p-3 border-1 border-200 border-round bg-teal-100">
          {{ formatText(question.explanation) }}
        </div>

      </div>
    </div>

    <div v-if="testFinished">
      <div v-if="isTestPassed" class="text-center m-4">
        <i class="pi pi-star-fill mx-2 text-orange-400"/>
        Поздравляем
        <i class="pi pi-star-fill mx-2 text-orange-400"/>
        <div>Вы успешно прошли тест</div>
      </div>
      <div v-else class="text-center m-4">
        😞 Сожалеем 😞
        <div>Для прохождения теста необходимо набрать более 70% верных ответов, а у вас {{userPercents}}%</div>
        <div>Не отчаивайтесь! Вы сможете пройти тест позднее 😊</div>
      </div>
      <div class="flex justify-content-center">
        <Knob v-model="testData.user_score" :value-color="isTestPassed?'teal':'#ff6767'" readonly :max="testData.total_score" :size="200"/>
      </div>
    </div>

    <div class="my-5 flex justify-content-center">
      <Button v-if="isAllQuestionsHasAnswer && !testFinished" label="Завершить тест" @click="submitTest" />
      <Button v-else-if="testFinished" label="Вернуться к списку" @click="$router.push('/tests')" />
    </div>

  </Container>


</template>

<script>
import Badge from "primevue/badge";
import Button from "primevue/button";
import Checkbox from "primevue/checkbox";
import Knob from "primevue/knob";
import Toast from 'primevue/toast';

import Container from "@/components/Container.vue";
import Menu from "@/components/Menu.vue";
import api from "@/services/api.js";

export default {
  name: "TestPassing",
  components: {
    Badge,
    Button,
    Checkbox,
    Container,
    Knob,
    Menu,
    Toast,
  },

  data() {
    return {
      testData: null,
      testFinished: false,
    }
  },

  mounted() {
    if (!this.loggedIn) this.$router.push("/login")

    api.get("questions/group/"+this.testID).then(
        res => this.testData = res.data,
        error => {
          let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
          this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
        }
    )
  },

  computed: {
    testID() {
      return this.$route.params.id
    },
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },

    isAllQuestionsHasAnswer() {
      for (const question of this.testData.questions) {
        if (!this.isQuestionHasAnswer(question)) return false;
      }
      return true
    },

    isTestPassed() {
      if (!this.testData.user_score || !this.testData.total_score) return false;
      return this.testData.user_score / this.testData.total_score > 0.7;
    },

    userPercents() {
      if (!this.testData.user_score || !this.testData.total_score) return 0;
      return Math.floor((this.testData.user_score / this.testData.total_score) * 100)
    },
  },

  methods: {
    formatText(text) {
      return text
    },

    answerCorrect(answer) {
      if (answer.true_valid === undefined) return true
      return !answer.is_valid || answer.true_valid === answer.is_valid
    },

    answerClasses(answer) {
      if (this.answerCorrect(answer)) {
        return ["p-3"]
      } else {
        return ["p-3", "border-left-3", "border-red-600"]
      }
    },

    submitTest() {
      api.post("questions/validate", this.testData).then(
          res => {
            this.testData = res.data;
            this.testFinished = true;
          },
          error => {
            let message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
            this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
          }
      )
    },

    isQuestionHasAnswer(question) {
      for (const answer of question.answers) {
        if (answer.is_valid) return true;
      }
      return false
    },

    questionCorrect(question) {
      for (const answer of question.answers) {
        if (!this.answerCorrect(answer)) return false;
      }
      return true
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