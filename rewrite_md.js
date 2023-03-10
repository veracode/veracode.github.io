const fs = require('fs');

// Read the Markdown file
const mdText = fs.readFileSync('readme.md', 'utf-8');

const lineArray = mdText.split("\n")
const numberOfLines = lineArray.length

var i
var topic = ""

for ( i = 0; i < numberOfLines; i++){
    //console.log('Line '+i+' '+lineArray[i])

    if ( lineArray[i].startsWith("##") ){
        topic =  lineArray[i].replace(/\ /g,"_")
        topic = topic.replace(/\//g,"_")
        topic = topic.replace(/\(/g,"")
        topic = topic.replace(/\)/g,"")
        topic = topic.replace(/\,/g,"")
        topic = topic.replace(/#{1,4}_/g,"").toLowerCase()
        console.log('Topic: '+topic)
    }

    if ( topic != "" && lineArray[i] != "" && lineArray[i].startsWith("##") != true){
        var item = lineArray[i].replace('](',' - ')
        item = item.replace(') ([',' - ')
        item = item.replace('](',' - ')
        item = item.replace('- [','')
        item = item.replace('))','')
        var content = item.split("\ -\ ")


        var fileContent = `---
layout: post
repolink: "${content[1]}"
title: "${content[0]}"
description: "${content[4]}"
author: "${content[2]}"
author-link: "${content[3]}"
content-type: "${topic}"
repo: "github"
repo_title: "${content[0]}"
---`
        console.log('Content: ')
        console.log(fileContent)
        if (!fs.existsSync('_'+topic)){
            fs.mkdirSync('_'+topic);
        }
        fs.writeFileSync(`./_${topic}/${content[0]}_${content[2]}.md`, fileContent)

    }
}