
def load_templates():
    specialization = input("Name of the specialization: ")
    course = input("Number of the course: ")
    week = input("Number of the week: ")

    dockerfile = """
    FROM frolvlad/alpine-miniconda3:python3.7

    RUN apk update && apk add libstdc++

    COPY requirements.txt .

    RUN pip install -r requirements.txt && \
    rm requirements.txt

    RUN mkdir /grader && \ 
    mkdir /grader/submission

    COPY data/ /grader/data/
    COPY entry.py /grader/entry.py
    COPY grader.py /grader/grader.py

    RUN chmod a+rwx /grader/

    WORKDIR /grader/

    ENTRYPOINT ["python", "entry.py"]
    """[1:]


    conf = f"""
    ASSIGNMENT_NAME = C{course}W{week}_Assignment
    IMAGE_NAME = {specialization}c{course}w{week}-grader
    TAG_ID = 1
    SUB_DIR = sub2
    MEMORY_LIMIT = 4096
    """[1:]


    makefile = """
    learner:
    [ "$(ls -A ./$(SUB_DIR))" ] && rm ./$(SUB_DIR)/* && echo "Deleted previous version"|| echo "Empty"
    cp sub2/submission.ipynb learner/$(ASSIGNMENT_NAME)_Solution.ipynb
    learner -fn learner/$(ASSIGNMENT_NAME)_Solution.ipynb 
    rm learner/$(ASSIGNMENT_NAME)_Solution.ipynb && rm learner/$(ASSIGNMENT_NAME)_Solution.py && rm learner/$(ASSIGNMENT_NAME).py

    build:
    docker build -t $(IMAGE_NAME):$(TAG_ID) .

    entry:
    docker run -it --rm --mount type=bind,source=$(PWD)/sub2,target=/shared/submission --mount type=bind,source=$(PWD),target=/grader/ --entrypoint ash $(IMAGE_NAME):$(TAG_ID)

    test:
    docker run -it --rm --mount type=bind,source=$(PWD)/sub2,target=/shared/submission --mount type=bind,source=$(PWD),target=/grader/ --entrypoint pytest $(IMAGE_NAME):$(TAG_ID)

    grade:
    gradethis $(PARTIDS) $(IMAGE_NAME):$(TAG_ID) $(SUB_DIR) $(MEMORY_LIMIT)

    mem:
    memthis $(PARTIDS)

    zip:
    zip -r $(IMAGE_NAME)$(TAG_ID).zip .

    clean:
    find . -maxdepth 1 -type f -name "*.zip" -exec rm {} +
    docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
    docker rm $(docker ps -qa --no-trunc --filter "status=exited")

    upload:
    coursera_autograder --timeout 1800 upload --grader-memory-limit $(MEMORY_LIMIT) --grading-timeout 1800 $(IMAGE_NAME)$(TAG_ID).zip $(COURSE_ID) $(ITEM_ID) $(PART_ID)

    move-zip:
    if [[ "$(OS)" == "Darwin" ]];    \
    then    \
    mv $(IMAGE_NAME)$(TAG_ID).zip /Users/andreszarta/Desktop/upload-temp;    \
    else    \
    mv $(IMAGE_NAME)$(TAG_ID).zip $$dlai/upload;    \
    fi

    move-learner:
    if [[ "$(OS)" == "Darwin" ]];    \
    then    \
    cp learner/$(ASSIGNMENT_NAME).ipynb /Users/andreszarta/Desktop/upload-temp;    \
    else    \
    cp learner/$(ASSIGNMENT_NAME).ipynb $$dlai/upload;    \
    fi
    """[1:]

    return dockerfile, makefile, conf

