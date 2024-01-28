import {UserTokens} from "@/user";

class TokenService {
    getLocalRefreshToken() {
        const user = this.getUserTokens();
        return user.refreshToken;
    }

    getLocalAccessToken() {
        const user = this.getUserTokens();
        return user.accessToken;
    }

    updateLocalAccessToken(token: string) {
        let user = this.getUserTokens();
        user.accessToken = token;
        localStorage.setItem("tokens", JSON.stringify(user));
    }

    set(tokens: UserTokens) {
        localStorage.setItem("tokens", JSON.stringify(tokens));
    }

    remove() {
        localStorage.removeItem("tokens");
    }

    getUserTokens(): UserTokens {
        const data = localStorage.getItem("tokens")
        if (data) {
            const jsonData = JSON.parse(data)
            return new UserTokens(jsonData.accessToken, jsonData.refreshToken)
        }
        return new UserTokens()
    }
}

export default new TokenService();