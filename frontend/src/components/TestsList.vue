<template>
  <Menu :user="userData"/>
  <Toast/>

  <Container>
    <div class="mx-2 m-5 search-panel">
      <div class="p-input-icon-left p-float-label m-2 search-input">
        <i class="pi pi-search" />
        <InputText v-model="search" style="width: 100%"/>
        <label for="chips">Поиск теста</label>
      </div>
      <div class="card p-fluid m-2 search-input">
        <div class="p-float-label">
          <Chips id="chips" v-model="selectedTags" style="width: 100%"/>
          <label for="chips">Укажите теги</label>
        </div>
      </div>
    </div>

    <div class="flex flex-column">
      <div v-for="test in filteredTests">
        <Card class="m-2">
          <template #title>
            <div class="flex align-items-center">
              <span class="mr-3">{{test.name}}</span><Button size="small" @click="$router.push('/test/'+test._id)" link label="Пройти"/>
            </div>
          </template>
          <template #content>
            <div class="m-0">
              <div v-if="test.description" class="mb-3">{{test.description}}</div>
              <div><i class="pi pi-user"/> {{test.username}}</div>
              <p v-if="test.completion_time_minutes > 0">Время прохождения: <i class="pi pi-stopwatch mr-1"></i>{{test.completion_time_minutes}} минут</p>
              <p v-else>Время на прохождение теста неограниченно</p>
              <p v-if="test.timeout_minutes > 0">Время для повторной попытки теста: <i class="pi pi-stopwatch mr-1"></i>{{test.timeout_minutes}} минут</p>
              <div>
                <Tag @click="selectedTags.push(tag)" v-for="tag in test.tags" :value="tag" class="mr-2 cursor-pointer"/>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </Container>

  <Footer/>
  <ScrollTop/>

</template>

<script>
import Button from "primevue/button";
import Card from "primevue/card";
import Chips from "primevue/chips";
import InputText from "primevue/inputtext";
import ScrollTop from "primevue/scrolltop";
import Tag from "primevue/tag";
import Toast from 'primevue/toast';

import Menu from "@/components/Menu.vue";
import Container from "@/components/Container.vue";
import api from "@/services/api.js";
import Footer from "@/components/Footer.vue";

export default {
  name: "TestsList",
  components: {
    Footer,
    Button,
    Card,
    Chips,
    Container,
    InputText,
    Menu,
    ScrollTop,
    Tag,
    Toast,
  },

  data() {
    return {
      allTests: [],
      search: "",
      selectedTags: [],
      userData: null,
    }
  },

  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
    filteredTests() {
      return this.allTests.filter(
          elem => {
            return this.filterByTestName(elem) && this.filterByTags(elem)
          }
      )
    }
  },

  mounted() {
    if (this.loggedIn) this.getMyself();

    api.get("questions/groups").then(
        res => {
          this.allTests = res.data
        },
        error => {
          let message = (error.response && error.response.data && error.response.data.detail) || error.message || error.toString();
          this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
        }
    )
  },

  methods: {
    filterByTestName(test) { return this.search.length === 0 || test.name.includes(this.search) },
    filterByTags(test) {
      return this.selectedTags.length === 0 || this.selectedTags.every(tag => {return test.tags.includes(tag)})
    },
    getMyself() {
      api.get("users/myself").then(
          res => this.userData = res.data,
          error => {
            let message = (error.response && error.response.data && error.response.data.detail) || error.response.data || error.toString();
            this.$toast.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
          }
      )
    }
  }
}
</script>

<style scoped>

.search-panel {
  display: flex;
}

.search-input {
  width: 50%
}

@media (width < 760px) {
  .search-panel {
    flex-wrap: wrap;
  }
  .search-input {
    width: 100%
  }
}

</style>