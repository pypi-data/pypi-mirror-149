FROM pytorch/pytorch
ARG pkg_version=
ENV pkg_version=$pkg_version
RUN apt update -y && \
    apt install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1-mesa-glx build-essential wget git
RUN mkdir -p /model_serving/module
RUN mkdir -p /model_serving/interface_class
RUN mkdir -p /mnt/model
WORKDIR /model_serving
ENV HOME=/model_serving
RUN python -m pip install --upgrade pip
RUN pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html
RUN python -m pip install sap-computer-vision-package${pkg_version}
COPY serve_models.py /model_serving/interface_class/serve_models.py
ENV MODEL_CONFIG_LIST_FILEPATH_YAML=/model_serving/model_serving.yaml
COPY requirements.txt /model_serving/requirements.txt
RUN python -m pip install -r /model_serving/requirements.txt
RUN chgrp -R nogroup /model_serving && \
    chmod -R 777 /model_serving
RUN chgrp -R nogroup /tmp && \
    chmod -R 777 /tmp && \
    chmod +t /tmp
CMD python /model_serving/interface_class/serve_models.py --model-kwarg iou_threshold $IOU_THRESHOLD $MODELS && cat $MODEL_CONFIG_LIST_FILEPATH_YAML && ls -larth /mnt/models/ && centaur
