from rest_framework import serializers

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version

import json
from rest_framework.renderers import JSONRenderer

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):
        # TODO
        # Validar o pacote, checar se ele existe na versão especificada.
        # Buscar a última versão caso ela não seja especificada pelo usuário.
        # Subir a exceção `serializers.ValidationError()` se o pacote não
        # for válido.
        return data


        found = False
        for i in data:
            if i == 'version':
                pack_ver = data[i]
                
                found = True

        if found == True:
            version_exist = version_exists(data["name"], pack_ver)
            
            if version_exist == True:
                return data
            else:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
        else:
            last = latest_version(data["name"])
            if last == None:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
            else:
                data['version'] = last
                return data


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        # TODO
        # Salvar o projeto e seus pacotes associados.
        #
        # Algumas referência para uso de models do Django:
        # - https://docs.djangoproject.com/en/3.2/topics/db/models/
        # - https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        packages = validated_data["packages"]
        return Project(name=validated_data["name"])
        projeto = Project.objects.create(name=validated_data["name"])
        leng_pack = len(packages)
        i = 0
        while i < leng_pack:
            package = PackageRelease.objects.create(name=packages[i]['name'], version=packages[i]['version'], project=projeto)
            i += 1
            projeto.save()g
        

        return projeto
