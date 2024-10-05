$(document).ready(function () {
    const socket = io();

    socket.on("init", function (ideas) {
        for (let idea of ideas) {
            addIdeaCard(idea);
        }
    });

    socket.on("idea", function (idea) {
        addIdeaCard(idea);
    });

    socket.on("update_vote", function (idea) {
        $(`#idea-${idea.id} .vote-count`).text(idea.votes);
    });

    socket.on("clear_board", function () {
        $("#ideas-container").empty();
    });

    $("#submit-ideas").click(function () {
        const inputText = $("#ideas-input").val();
        const parsedIdeas = parseInput(inputText);

        for (const idea of parsedIdeas) {
            socket.emit("submit_idea", idea);
        }
    });

    $("#clear-board").click(function () {
        socket.emit("clear_board");
    });

    function addIdeaCard(idea) {
        const card = $("<div>")
            .addClass("idea-card")
            .attr("id", `idea-${idea.id}`);
        const title = $("<h3>").text(idea.title);
        const descriptionList = $("<ul>").addClass("card-description list-unstyled");

        if (idea.description) {
            const descriptionLines = idea.description.split("\n");
            for (const line of descriptionLines) {
                if (line.trim() !== "") {
                    const listItem = $("<li>").text(line);
                    descriptionList.append(listItem);
                }
            }
        }

        const voteButtons = $("<div>").addClass("vote-buttons");
        const upvoteButton = $("<button>")
            .text("Upvote")
            .addClass("upvote-button");
        const downvoteButton = $("<button>")
            .text("Downvote")
            .addClass("downvote-button");
        const voteCount = $("<span>").text(idea.votes).addClass("vote-count");

        upvoteButton.click(function () {
            socket.emit("vote", { id: idea.id, change: 1 });
        });

        downvoteButton.click(function () {
            socket.emit("vote", { id: idea.id, change: -1 });
        });

        voteButtons.append(upvoteButton, voteCount, downvoteButton);
        card.append(title, descriptionList, voteButtons);
        $("#ideas-container").append(card);
    }

    function parseInput(input) {
        let lines = input.trim().split("\n");
        let ideas = [];
        let currentIdea = null;

        for (let line of lines) {
            if (line.startsWith(" ") || line.startsWith("\t")) {
                if (currentIdea) {
                    currentIdea.description += "\n" + line.trim();
                }
            } else {
                if (currentIdea) {
                    ideas.push(currentIdea);
                }
                currentIdea = { title: line.trim(), description: "" };
            }
        }

        if (currentIdea) {
            ideas.push(currentIdea);
        }

        return ideas;
    }
});
