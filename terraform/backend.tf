terraform {
  backend "s3" {
    bucket = "terraform-state-flaskbb-corise-chrisbloom7"
    key    = "core/terraform.tfstate"
    region = "us-east-1"
  }
}
