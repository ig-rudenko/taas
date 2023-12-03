let themeStore = localStorage.getItem("userTheme")

if (!themeStore) {
    themeStore = "lara-light-teal"
}

function getOtherTheme(theme) {
    if (theme === "lara-light-teal") {
        return  "lara-dark-teal"
    } else {
        return  "lara-light-teal"
    }
}


const themeSwitch = {
    current: themeStore,
    other: getOtherTheme(themeStore),
    newTheme(theme) {
        localStorage.setItem("userTheme", theme)
        this.current = theme
        this.other = getOtherTheme(theme)
    }
}


export default themeSwitch
