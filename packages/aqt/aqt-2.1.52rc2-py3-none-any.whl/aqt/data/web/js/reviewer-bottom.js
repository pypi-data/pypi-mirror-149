"use strict";
/* Copyright: Ankitects Pty Ltd and contributors
 * License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html */
/* eslint
@typescript-eslint/no-unused-vars: "off",
*/
let time; // set in python code
let maxTime = 0;
document.addEventListener("DOMContentLoaded", () => {
    updateTime();
    setInterval(function () {
        time += 1;
        updateTime();
    }, 1000);
});
function updateTime() {
    const timeNode = document.getElementById("time");
    if (maxTime === 0) {
        timeNode.textContent = "";
        return;
    }
    time = Math.min(maxTime, time);
    const m = Math.floor(time / 60);
    const s = time % 60;
    const sStr = String(s).padStart(2, "0");
    const timeString = `${m}:${sStr}`;
    if (maxTime === time) {
        timeNode.innerHTML = `<font color=red>${timeString}</font>`;
    }
    else {
        timeNode.textContent = timeString;
    }
}
function showQuestion(txt, maxTime_) {
    showAnswer(txt);
    time = 0;
    maxTime = maxTime_;
}
function showAnswer(txt) {
    document.getElementById("middle").innerHTML = txt;
}
function selectedAnswerButton() {
    const node = document.activeElement;
    if (!node) {
        return;
    }
    return node.dataset.ease;
}
