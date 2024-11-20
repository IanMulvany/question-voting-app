$(document).ready(function () {
    const socket = io();
    const addedIdeaIds = new Set();

    // Initialize ideas from the server
    socket.on("init", function (ideas) {
        console.log("Received init event with ideas:", ideas);
        $("#ideas-container").empty();

        for (let idea of ideas) {
            if (!addedIdeaIds.has(idea.id)) {
                addIdeaCard(idea);
                addedIdeaIds.add(idea.id);
            } else {
                console.log(`Idea ID ${idea.id} already added, skipping.`);
            }
        }

        if (ideas.length > 0) {
            const firstIdea = ideas[0];
            $("#submitted-question").show();
            $("#user-question-title").text(firstIdea.title);
            $("#user-question-description").empty();

            if (firstIdea.description) {
                const descriptionLines = firstIdea.description.split("\n");
                for (const line of descriptionLines) {
                    if (line.trim() !== "") {
                        const listItem = $("<li>").text(line);
                        $("#user-question-description").append(listItem);
                    }
                }
            }
        }
    });

    // Update vote count for an idea
    socket.on("update_vote", function (idea) {
        const voteElement = $(`#idea-${idea.id} .vote-count`);
        if (voteElement.length > 0) {
            voteElement.text(idea.votes);
        } else {
            console.warn(`Idea ID ${idea.id} missing; re-adding.`);
            addIdeaCard(idea);
            addedIdeaIds.add(idea.id);
        }
    });

    // Add a new idea dynamically
    socket.on("idea", function (idea) {
        if (!addedIdeaIds.has(idea.id)) {
            addIdeaCard(idea);
            addedIdeaIds.add(idea.id);
        }
    });

    // Clear all ideas from the board
    socket.on("clear_board", function () {
        $("#ideas-container").empty();
        addedIdeaIds.clear();
    });

    // Submit new ideas
    $("#submit-ideas").off("click").on("click", function () {
        const inputText = $("#ideas-input").val();
        const parsedIdeas = parseInput(inputText);

        for (const idea of parsedIdeas) {
            socket.emit("submit_idea", idea);
        }

        $("#ideas-input").val(''); // Clear the input after submission
    });

    // Clear the board
    $("#clear-board").click(function () {
        socket.emit("clear_board");
    });

    // Add idea card to the UI
    function addIdeaCard(idea) {
        if ($(`#idea-${idea.id}`).length > 0) {
            return;
        }

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
        const voteCount = $("<span>")
            .text(idea.votes)
            .addClass("vote-count");

        voteButtons.append(upvoteButton, voteCount, downvoteButton);
        card.append(title, descriptionList, voteButtons);
        $("#ideas-container").append(card);
    }

    // Handle upvotes and downvotes dynamically
    $("#ideas-container").on("click", ".upvote-button", function () {
        const ideaId = $(this).closest(".idea-card").attr("id").split("-")[1];
        console.log("Upvote clicked for idea:", ideaId);
        socket.emit("vote", { id: ideaId, change: 1 });
    });

    $("#ideas-container").on("click", ".downvote-button", function () {
        const ideaId = $(this).closest(".idea-card").attr("id").split("-")[1];
        console.log("Downvote clicked for idea:", ideaId);
        socket.emit("vote", { id: ideaId, change: -1 });
    });

    // Parse input text into idea objects
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

    // Log reconnections
    socket.on("reconnect", (attemptNumber) => {
        console.log(`Reconnected to the server after ${attemptNumber} attempts.`);
    });
});