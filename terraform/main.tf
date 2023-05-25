terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "slack_data_store" {
  bucket = "slack-data-store"
}

resource "aws_iam_policy" "policy" {
  name        = "data-processor-sm-policy"
  description = "A policy for the data processor state machine"
  policy      = "${file("stateMachinePolicy.json")}"
}

resource "aws_iam_role" "sm_role" {
  name               = "sm-role"
  assume_role_policy = "${file("assumerolepolicy.json")}"
}

resource "aws_iam_policy_attachment" "test-attach" {
  name       = "test-attachment"
  roles      = ["${aws_iam_role.sm_role.name}"]
  policy_arn = "${aws_iam_policy.policy.arn}"
}