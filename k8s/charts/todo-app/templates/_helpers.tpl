{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s" $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "todo-app.backend.selectorLabels" -}}
app: todo-app
component: backend
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "todo-app.frontend.selectorLabels" -}}
app: todo-app
component: frontend
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-app.backend.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.backend.selectorLabels" . }}
tier: api
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-app.frontend.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.frontend.selectorLabels" . }}
tier: web
{{- end }}
