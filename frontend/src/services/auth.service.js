import api from "./api";
import TokenService from "./token.service";

class AuthService {
    login({ username, password }) {
        return api
            .post("/auth/token", {
                username,
                password
            })
            .then(
                response => {
                    if (response.data.accessToken) {
                        TokenService.setUser(response.data);
                    }

                    return response.data;
                },
                reason => {
                    console.log(reason)
                    return reason
                }
            );
    }

    logout() {
        TokenService.removeUser();
    }

    register({ username, email, password }) {
        return api.post("/auth/register", {
            username,
            email,
            password
        });
    }
}

export default new AuthService();