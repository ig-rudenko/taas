<template>
  <h1>Создание нового теста</h1>
  <div v-if="userData && userData.can_create_tests">
    <div>
      <div class="flex flex-column gap-2 my-2">
        <label for="testName">Название теста</label>
        <InputText id="testName" v-model="testData.name"/>
      </div>
      <div class="flex flex-column gap-2 my-2">
        <label for="testDesc">Описание теста</label>
        <InputText id="testDesc" v-model="testData.description"/>
      </div>
      <div class="flex flex-column gap-2 my-2 p-fluid">
        <label for="testTags">Укажите теги для теста</label>
        <Chips id="testTags" v-model="testData.tags" aria-describedby="testTags-help" />
        <small id="testTags-help">Вы можете указать уровень сложности теста через теги `easy`, `medium`, `hard`.</small>
      </div>

      <div class="flex flex-wrap mt-4">
        <div class="flex flex-column gap-2 m-2">
          <label for="timeout_minutes" class="block mb-2">Кол-во минут ожидания для <br>повторного прохождения теста</label>
          <InputNumber v-model="testData.timeout_minutes" inputId="timeout_minutes" mode="decimal" showButtons :min="0" aria-describedby="timeout_minutes-help" />
          <small id="timeout_minutes-help">`0` - без ограничений</small>
        </div>
        <div class="flex flex-column gap-2 m-2">
          <label for="completion_time_minutes" class="block mb-2"><br>Кол-во минут на прохождение теста</label>
          <InputNumber v-model="testData.completion_time_minutes" inputId="completion_time_minutes" mode="decimal" showButtons :min="0" aria-describedby="completion_time_minutes-help" />
          <small id="completion_time_minutes-help">`0` - без ограничений</small>
        </div>
      </div>
    </div>


    <div v-for="(question, qID) in testData.questions" class="relative">
      <div :id="'question-'+(qID+1)" class="absolute" style="top: -100px"></div>

      <div class="p-5 my-5 border-round border-1 border-300 hover:shadow-2 p-card">

        <Badge size="xlarge" class="absolute question-number" :value="'# ' + (qID + 1)" />
        <Button @click="testData.deleteQuestion(qID)" class="absolute question-delete" icon="pi pi-times" size="small" severity="danger" rounded raised aria-label="Cancel" />

        <!-- Вопрос -->
        <div class="my-2 md:font-normal">
          <div class="flex flex-column gap-2 my-2">
            <label :for="'q-text-'+qID">Описание вопроса</label>
            <Textarea :id="'q-text-'+qID" v-model="question.text" rows="8"/>
          </div>
        </div>

        <!-- Варианты ответа -->
        <div v-for="(answer, aID) in question.answers" class="flex flex-column gap-2 my-2">
          <div class="mt-2 flex flex-wrap justify-content-between align-items-center">
            <div>
              <span class="mr-3">Вариант ответа {{aID+1}}</span>
              <Checkbox class="mr-3" v-model="answer.is_valid" :binary="true"/>
              <span v-if="answer.is_valid">Верный</span>
            </div>
            <div>
              <Button @click="question.deleteAnswer(aID)" icon="pi pi-times" size="small" severity="danger" rounded outlined aria-label="Cancel" />
            </div>
          </div>
          <Textarea v-model="answer.text" rows="5"/>
        </div>

        <div>
          <Button label="Добавить вариант ответа" size="small" severity="info" @click="question.addAnswer()"/>
        </div>

        <!-- Объяснение верного ответа -->
        <div class="mt-4 p-3 border-1 border-200 border-round p-message-success p-message">
          <div class="flex flex-column gap-2 my-2">
            <label :for="'exp-'+qID">Объяснение верного ответа</label>
            <Textarea :id="'exp-'+qID" v-model="question.explanation" rows="6"/>
          </div>
        </div>

      </div>
    </div>

    <div class="flex justify-content-between">
      <Button label="Добавить новый вопрос" size="small" severity="info" @click="testData.addQuestion()"/>

      <Button :label="submitButtonLabel" size="small" @click="submitTest"/>
    </div>

  </div>
  <div v-else>
    <h2>У вас нет возможности создавать/обновлять тесты</h2>
  </div>

</template>

<script lang="ts">
import Badge from "primevue/badge";
import Button from "primevue/button";
import Checkbox from "primevue/checkbox";
import Chips from "primevue/chips";
import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Textarea from "primevue/textarea";
import Toast from "primevue/toast";

import api from "@/services/api.js";
import {FullTest, User, Question, Answer} from "@/types.ts";

export default {
  name: "CreateTest",
  components: {
    Badge,
    Button,
    Checkbox,
    Chips,
    InputNumber,
    InputText,
    Message,
    Textarea,
    Toast,
  },

  props: {
    userData: {required: true, type: User},
    createMode: {required: true, type: Boolean},
    testId: {required: false, type: String},
  },

  data() {
    return {
      testData: new FullTest(
        "",
        "",
        0,
        0,
        ["easy"],
        [
          new Question(
            "",
            [
              new Answer("Ответ 1", false),
              new Answer("Верный ответ", true)
            ],
            "",
            ""
          )
        ],
      ),
    }
  },

  mounted() {
    if (!this.createMode) this.getTestData()
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
    submitButtonLabel() {
      return this.createMode?"Создать тест":"Обновить тест"
    },
    httpSubmitMethod() {
      return this.createMode?"post":"put"
    },
    httpSubmitUrl() {
      return this.createMode?"questions/groups":"questions/group/"+this.testId
    },
    responseSuccessText() {
      return this.createMode?"Тест добавлен успешно!":"Тест обновлен успешно!"
    },
  },

  methods: {

    getTestData() {
      api.get("questions/group/"+this.testId+"/full-access").then(
          res => this.testData = new FullTest(...res.data),
          error => this.handleError(error)
      )
    },

    submitTest() {
      api[this.httpSubmitMethod](this.httpSubmitUrl, this.testData).then(
          () => {
            this.$toast.add({ severity: 'success', summary: 'Success', detail: this.responseSuccessText, life: 3000 });
            if (this.createMode) this.$router.push("/tests");
          },
          error => this.handleError(error)
      )
    },

    handleError(error) {
      let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
      this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
    },

  },

}
</script>

<style scoped>

.question-number {
  top: -20px;
  left: -20px;
}

@media (width < 1111px) {
  .question-number {
    left: -1px;
  }
}

.question-delete {
  top: -20px;
  right: -20px;
}

@media (width < 1111px) {
  .question-delete {
    right: -1px;
  }
}

</style>