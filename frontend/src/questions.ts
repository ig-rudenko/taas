class Answer {
    constructor(
        public text: string = "",
        public isValid: boolean = false,
        public trueValid: boolean = true,
    ) {}

    public get isCorrect() {
        if (this.trueValid === undefined) return true
        return !this.isValid || this.trueValid === this.isValid
    }
}

class Question {
    constructor(
        public text: string = "",
        public answers: Array<Answer> = [new Answer()],
        public image: string = "",
        public explanation: string = "",
    ) {}

    addAnswer(): void {
        this.answers.push(new Answer())
    }

    deleteAnswer(answerID: number): void {
        this.answers.splice(answerID, 1)
    }
}


class TestAbout {
    constructor(
        public _id: string,
        public name: string,
        public description: string,
        public username: string,
        public completionTimeMinutes: number,
        public timeoutMinutes: number,
        public tags: Array<string>
    ) {}
}


class FullTest extends TestAbout {
    questions: Array<Question>
    constructor(name: string,
                description: string,
                completionTimeMinutes: number,
                timeoutMinutes: number,
                tags: Array<string>,
                questions: Array<Question>
    ) {
        super("", name, description, null, completionTimeMinutes, timeoutMinutes, tags);
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


class TestResultMixin {

    constructor(
        public userScore: number = null,
        public totalScore: number = null
    ) {}

    public get percents(): number {
        return Math.floor((this.userScore / this.totalScore) * 100)
    }

    public get passedSuccessfully(): boolean {
        return this.userScore / this.totalScore > 0.7
    }
}


class TestForPassing extends TestResultMixin {
    constructor(
        public _id: string,
        public name: string,
        public description: string,
        public completionTimeSeconds: number,
        public questions: Array<Question>,
        public userScore: number,
        public totalScore: number,
    ) {
        super(userScore, totalScore)
    }

}

class PassedQuestion extends TestResultMixin {
    createdAt: Date
    questionGroupId: string
    questionGroupName: string
    totalScore: number
    userId: string
    userScore: number
    constructor(createdAt: string, questionGroupId: string, questionGroupName: string,
                totalScore: number, userId: string, userScore: number) {
        super(userScore, totalScore)
        this.createdAt = new Date(createdAt)
        this.questionGroupId= questionGroupId
        this.questionGroupName= questionGroupName
        this.userId= userId
    }

    public get dateString(): string {
        return new Intl.DateTimeFormat(
            "ru",
            {day: "numeric", month: "long", year: "numeric", hour: "numeric", minute: "numeric"}
        ).format(this.createdAt)
    }

}

function createNewQuestions(data: Array<any>): Array<Question> {
    let questions: Array<Question> = []
    for (const questionData of data) {
        let answers: Array<Answer> = []
        for (const answerData of questionData.answers) {
            answers.push(new Answer(answerData.text, answerData.isValid, answerData.trueValid))
        }
        questions.push(new Question(questionData.text, answers, questionData.image, questionData.explanation))
    }
    return questions
}


function createNewTestForPassing(data: any): TestForPassing {
    return new TestForPassing(
        data._id,
        data.name,
        data.description,
        data.completionTimeSeconds,
        createNewQuestions(data.questions),
        data.userScore,
        data.totalScore,
    )
}

function createNewFullTest(data: any): FullTest {
    return new FullTest(
        data.name,
        data.description,
        data.completionTimeMinutes,
        data.timeoutMinutes,
        data.tags,
        createNewQuestions(data.questions),
    )
}


function createNewTestAboutList(data: Array<any>): Array<TestAbout> {
    let res: Array<TestAbout> = []
    for (const testData of data) {
        res.push(
            new TestAbout(testData._id, testData.name, testData.description, testData.username,
                testData.completionTimeMinutes, testData.timeoutMinutes, testData.tags)
        )
    }
    return res
}

export {
    TestAbout,FullTest,Question,Answer,PassedQuestion,TestForPassing,
    createNewTestAboutList,createNewFullTest,createNewTestForPassing
}
