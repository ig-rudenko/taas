export class UserOpenedQuestionTimes {
    constructor(
        public startTime: string,
        public expireTime: string,
        public nextTryTime: string,
        public finishedTime?: string | null,
    ) {}
}