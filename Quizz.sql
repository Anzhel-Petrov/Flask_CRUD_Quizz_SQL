DROP TABLE questions;
DROP TABLE answers;

CREATE TABLE questions
(
  question_id      INT           NOT NULL IDENTITY(1,1),
  question_text    VARCHAR(100)  NOT NULL
);
ALTER TABLE questions
ADD CONSTRAINT pk_questions PRIMARY KEY (question_id);

CREATE TABLE answers
(
  answer_id          INT           NOT NULL IDENTITY(1,1),
  question_id        INT           NOT NULL ,
  question_answer    VARCHAR(100)  NOT NULL ,
  is_correct         BIT		   NOT NULL
);
ALTER TABLE answers
ADD CONSTRAINT pk_answers PRIMARY KEY (answer_id);
ALTER TABLE questions 
ADD CONSTRAINT fk_answers_questions FOREIGN KEY (question_id) REFERENCES questions (question_id);


INSERT INTO questions VALUES ('What year was Bulgaria founded?');
INSERT INTO questions VALUES ('How long does the sunlight travel to Earth?');
INSERT INTO questions VALUES ('What is the capital of Bulgaria?');
INSERT INTO questions VALUES ('What is the capital of Poland?');

INSERT INTO answers VALUES (1, '815', 0);
INSERT INTO answers VALUES (1, '681', 1);
INSERT INTO answers VALUES (1, '903', 0);
INSERT INTO answers VALUES (1, '1396', 0);
INSERT INTO answers VALUES (2, '47 seconds', 0);
INSERT INTO answers VALUES (2, '2 minutes', 0);
INSERT INTO answers VALUES (2, '8 seconds', 1);
INSERT INTO answers VALUES (2, '27 seconds', 0);
INSERT INTO answers VALUES (3, 'Sofia', 1);
INSERT INTO answers VALUES (3, 'Plovdiv', 0);
INSERT INTO answers VALUES (3, 'Bucharest', 0);
INSERT INTO answers VALUES (3, 'Varna', 0);
INSERT INTO answers VALUES (4, 'Riga', 0);
INSERT INTO answers VALUES (4, 'Talin', 0);
INSERT INTO answers VALUES (4, 'Warsaw', 1);
INSERT INTO answers VALUES (4, 'Sofia', 0);

SELECT * FROM questions;
SELECT * FROM answers;

SELECT question_text,question_answer
FROM questions INNER JOIN answers ON
questions.question_id = answers.question_id