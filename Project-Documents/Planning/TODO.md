# Aigency Checklist Roadmap

August 25, 2024
---

# Milestone 1: Foundational Services

## AI Coder Agents / Frameworks

- [ ] Deploy Dask for distributed computing:
  - [ ] Set up Dask scheduler
  - [ ] Configure Dask workers
  - [ ] Integrate with project codebase
- [ ] Deploy vLLM for language processing:
  - [ ] Set up vLLM server
  - [ ] Configure vLLM API
  - [ ] Integrate with project codebase
- [ ] Deploy Ollama for knowledge graph management:
  - [ ] Set up Ollama server
  - [ ] Configure Ollama API
  - [ ] Integrate with project codebase

## Tailnet for Remote Access

- [ ] Set up Tailscale for secure, encrypted connections:
  - [ ] Configure Tailscale authentication
  - [ ] Set up Tailscale network
- [ ] Configure access controls for each microservice:
  - [ ] Define access roles and permissions
  - [ ] Implement access controls for each microservice

## Agentic Documentation

- [ ] Install open source documentation project for use as our app documentation:
  - [ ] Evaluate phiData for documentation management
  - [ ] Evaluate crewai for documentation management
  - [ ] Evaluate agile coder for documentation management
  - [ ] Evaluate chatDev related projects for documentation management
- [ ] Assign a crew of agents to create and maintain project documentation:
  - [ ] Define roles and responsibilities for documentation agents
  - [ ] Create agents to the documentation app

## Micro Frontend for Atomic Design and Branding

- [ ] Design and implement a user interface for the project's branding and design elements:
  - [ ] Create a style guide for the project
  - [ ] Implement the style guide in the micro frontend
- [ ] Integrate with the project's atomic design system:
  - [ ] Set up atomic design components
  - [ ] Use atomic design components in the micro frontend

## Micro Frontend for Observability

- [ ] Set up Grafana for visualization of metrics and logs:
  - [ ] Configure Grafana data sources
  - [ ] Create Grafana dashboards
- [ ] Integrate Prometheus for service monitoring:
  - [ ] Configure Prometheus scrape targets
  - [ ] Set up Prometheus alerts
- [ ] Add other observability tools as needed:
  - [ ] Research and evaluate additional tools
  - [ ] Integrate additional tools into the micro frontend

## Micro Frontend for Agent Interaction and Project Management

- [ ] Design and implement a user interface for agent interaction and project tracking:
  - [ ] Create a user interface for agent interaction
  - [ ] Implement project tracking features
- [ ] Integrate with project management tools for task assignment and tracking:
  - [ ] Research and evaluate project management tools
  - [ ] Integrate the chosen tool into the micro frontend
- [ ] Implement a dashboard for project overview and progress tracking:
  - [ ] Design and implement the dashboard
  - [ ] Integrate with project tracking features

# Milestone 2: Zero-Dollar Deployment

## Platform Selection

- [ ] Research and evaluate free tier options for IBM Cloud and AWS:
  - [ ] Compare features and limitations
  - [ ] Choose a primary platform
- [ ] Consider additional platforms for specific use cases:
  - [ ] Railway
  - [ ] Fly.io
  - [ ] Render
  - [ ] Heroku

## DevOps and CI/CD Pipeline

- [ ] Set up a Git flow strategy:
  - [ ] Implement Conventional Commits with Husky
  - [ ] Configure GPTLint and Commitlint
  - [ ] Integrate Devmoji and Commitizen
- [ ] Implement testing with a goal of 70% code coverage:
  - [ ] Choose a testing framework
  - [ ] Write unit tests and integration tests
- [ ] Set up CI/CD pipeline with GitHub Actions:
  - [ ] Configure pipeline for automated testing and deployment
  - [ ] Integrate CodeCov for code coverage reporting

## Dependency Management and Security

- [ ] Implement dependency management with GitHub Marketplace apps:
  - [ ] Choose a dependency management tool
  - [ ] Configure tool for automated dependency updates
- [ ] Integrate security tools for vulnerability scanning and monitoring:
  - [ ] Choose a security tool
  - [ ] Configure tool for automated scanning and monitoring

## High Availability and Production Deployment

- [ ] Deploy the application to the chosen platform:
  - [ ] Configure deployment scripts
  - [ ] Deploy the application
- [ ] Ensure high availability and scalability:
  - [ ] Configure load balancing and autoscaling
  - [ ] Monitor application performance

## Stretch Goal: Shared Development Space

- [ ] Research and evaluate options for shared development spaces:
  - [ ] Lightning.ai
  - [ ] Similar platforms
- [ ] Implement a shared development space:
  - [ ] Configure the chosen platform
  - [ ] Integrate with the project codebase

## Milestone 3: Self Learning, Crowd Sourced Agentic Blog
- [ ] Design and develop a blogging platform:
  - [ ] Choose a suitable tech stack and framework
  - [ ] Design a data system for storing and retrieving content
  - [ ] Implement user authentication and authorization for human reviewers
- [ ] Create an agent crew for content generation and editing:
  - [ ] Develop AI-powered agents for research, writing, and editing
  - [ ] Train agents on a dataset of relevant content and topics
  - [ ] Implement a workflow for agent collaboration and content review
- [ ] Develop a system for human review and feedback:
  - [ ] Implement a review process for human oversight and feedback
  - [ ] Develop a user interface for human reviewers to provide feedback and ratings
  - [ ] Integrate feedback into the agent workflow for continuous improvement
- [ ] Develop a system for reader influence and feedback:
  - [ ] Implement a rating and commenting system for readers
  - [ ] Analyze reader feedback to inform future content direction
  - [ ] Integrate machine learning to adapt content based on reader preferences
- [ ] Ensure content quality and accuracy:
  - [ ] Implement fact-checking and verification processes
  - [ ] Establish guidelines for AI-generated content
  - [ ] Provide training and resources for human reviewers and editors
- [ ] Launch and promote the blog:
  - [ ] Plan and execute a launch strategy
  - [ ] Develop a content calendar and posting schedule
  - [ ] Promote the blog through social media and other channels



