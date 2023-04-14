import { faker } from "@faker-js/faker";
import * as fs from "fs/promises";

function choose(choices) {
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

let users = [];
let posts = [];

function createRandomUser() {
  faker.locale = choose(["fa", "en"]);
  var first_name = faker.name.firstName();
  faker.locale = choose(["fa", "en"]);
  var description = faker.lorem.sentence();
  faker.locale = "en";
  return {
    first_name: first_name,
    username: faker.internet.userName(),
    email: faker.internet.email(),
    photo: faker.image.avatar(),
    description: description,
    password: faker.internet.password(),
    date_of_birth: faker.date.birthdate(),
  };
}

function createRandomPost() {
  faker.locale = choose(["fa", "en"]);
  var description = faker.lorem.paragraphs();
  faker.locale = "en";
  return {
    photo: faker.image.image(),
    description: description,
    created: faker.date.past(),
    tag: choose(["fake", "فیک"]),
  };
}

Array.from({ length: 20 }).forEach(() => {
  users.push(createRandomUser());
});

Array.from({ length: 100 }).forEach(() => {
  posts.push(createRandomPost());
});

let usersJsonContent = JSON.stringify(users);
let postsJsonContent = JSON.stringify(posts);

fs.writeFile("./users.json", usersJsonContent, "utf8", function (err) {
  if (err) {
    return console.log(err);
  }
  console.log("The file was saved!");
});

fs.writeFile("./posts.json", postsJsonContent, "utf8", function (err) {
  if (err) {
    return console.log(err);
  }
  console.log("The file was saved!");
});
