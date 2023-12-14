class Answer {
    text: string
    is_valid: boolean
    constructor(text: string = "", is_valid: boolean = false) {
        this.text = text
        this.is_valid = is_valid
    }
}

class Question {
    text: string
    answers: Array<Answer>
    image: string
    explanation: string
    constructor(text: string = "", answers: Array<Answer> = [new Answer()], image: string = "", explanation: string = "") {
        this.text = text
        this.answers = answers
        this.image = image
        this.explanation = explanation
    }

    addAnswer(): void {
        this.answers.push(new Answer())
    }

    deleteAnswer(answerID: number): void {
        this.answers.splice(answerID, 1)
    }
}


class TestMin {
    _id: string = ""
    name: string
    description: string
    username: string = null
    completion_time_minutes: number
    timeout_minutes: number
    tags: Array<string>
    constructor(_id: string = "", name: string = "", description: string = "", username?: string, completion_time_minutes: number = 0,
                timeout_minutes: number = 0, tags?: Array<string>) {
        this._id = _id
        this.name = name
        this.description = description
        this.username = username
        this.completion_time_minutes = completion_time_minutes
        this.timeout_minutes = timeout_minutes
        this.tags = tags
    }
}


class FullTest extends TestMin {
    questions: Array<Question>
    constructor(name: string, description: string, completion_time_minutes: number,
                timeout_minutes: number, tags: Array<string>, questions: Array<Question>) {
        super("", name, description, null, completion_time_minutes, timeout_minutes, tags);
        this.questions = questions
    }

    addQuestion(): void {
        this.questions.push(
          new Question(
            "",
            [
              new Answer("Ответ 1", false),
              new Answer("Верный ответ", true)
            ],
            "",
            ""
          )
      )
    }

    deleteQuestion(questionID: number): void {
        this.questions.splice(questionID, 1)
    }
}

class LoginUserIsValid {
    username: boolean = true
    password: boolean = true
}

class RegisterUserIsValid extends LoginUserIsValid {
    email: boolean = true
}



class LoginUser {
    username: string
    password: string
    readonly valid: LoginUserIsValid

    constructor(username: string = "", password: string = "") {
        this.username = username
        this.password = password
        this.valid = new LoginUserIsValid()
    }

    public get isValid(): boolean {
      this.valid.username = this.username.length > 2
      this.valid.password = this.password.length > 8
      return this.valid.username && this.valid.password
    }

}

class RegisterUser extends LoginUser {
    email: string
    readonly valid: RegisterUserIsValid

    constructor(username: string = "", email: string = "", password: string = "") {
        super(username, password)
        this.email = email
        this.valid = new RegisterUserIsValid()
    }

    public get isValid(): boolean {
      this.valid.username = this.username.length > 2
      this.valid.email = this.email.length > 0 && this.email.indexOf("@") > 0
      this.valid.password = this.password.length > 8
      return this.valid.username && this.valid.email && this.valid.password
    }

}

class User {
    _id: string
    username: string
    can_create_tests: boolean
    is_superuser: boolean
    first_name: string
    // Фамилия
    surname: string
    last_name: string

    constructor(_id: string, username: string, can_create_tests: boolean, is_superuser: boolean, first_name: string,
                surname: string, last_name: string) {
        this._id = _id
        this.username = username
        this.can_create_tests = can_create_tests
        this.is_superuser = is_superuser
        this.first_name = first_name
        this.surname = surname
        this.last_name = last_name
    }
}

export {TestMin, User, LoginUser, RegisterUser, FullTest, Question, Answer}
