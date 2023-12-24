import Prism from 'prismjs';
import 'prismjs/themes/prism.css';
import 'prismjs/components/prism-javascript.min.js';
import 'prismjs/components/prism-python.min.js';
import "prismjs/components/prism-go.min.js"


function format_to_html(str: string): string {
    let n_re = new RegExp('\n', 'g');
    return str.replace(n_re, "<br>")
}

function highlightTextToCode(text: string, languageCode: string): string {
    try {
        let formattedText = "<code>"
        let textLines = text.split('\n')
        if (!textLines.length) {
            formattedText += text + "</code>"
            return formattedText
        }

        for (const textElement of textLines) {
            let noSpaces = textElement.match(/(^\s*)(.*)$/)
            formattedText += noSpaces[1].replace(RegExp(' ', "g"), "&nbsp;")
            formattedText += Prism.highlight(noSpaces[2], Prism.languages[languageCode], languageCode);
            formattedText += "<br>"
        }
        formattedText += "</code>"
        return formattedText
    } catch (e) {
        console.log(e)
        return "<code>" + text + "</code>"
    }
}


function findCodeBlocksAndFormat(text: string): string {
    const blocks = text.match(RegExp('```(.*?)```|(.+?)(?=```)', "sg"))
    if (!blocks) return format_to_html(text);

    let result = ""
    for (let i = 0; i < blocks.length; i++) {
        let language = blocks[i].match(/```(\S+)\n(.*)```/s)
        if (language) {
            result += highlightTextToCode(language[2], language[1])
        } else {
            result += format_to_html(blocks[i])
        }
    }
    return result
}

export {findCodeBlocksAndFormat, format_to_html}
