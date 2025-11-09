import streamlit as st
from src.utils import api_keys, file_operations, caching
from src.analysis import resume_analyzer, jd_analyzer
from src.web import job_search
import os
import google.generativeai as genai
from datetime import datetime

def main():
    st.title("Job Search AI Assistant")

    # Initialize session state
    if 'resume_path' not in st.session_state:
        st.session_state.resume_path = file_operations.get_cached_user_file("resume")
    if 'jd_path' not in st.session_state:
        st.session_state.jd_path = file_operations.get_cached_user_file("jd")
    if 'latex_template_path' not in st.session_state:
        st.session_state.latex_template_path = file_operations.get_cached_user_file("template")
    if 'resume_analysis' not in st.session_state:
        st.session_state.resume_analysis = None
    if 'jd_analysis' not in st.session_state:
        st.session_state.jd_analysis = None
    if 'found_jobs' not in st.session_state:
        st.session_state.found_jobs = []

        # API Key Management
    st.sidebar.title("API Keys")
    gemini_api_key_from_file = api_keys.load_api_key("Gemini")
    gemini_api_key = st.sidebar.text_input("Gemini API Key", value=gemini_api_key_from_file, type="password")
    if gemini_api_key and gemini_api_key != gemini_api_key_from_file:
        api_keys.save_api_key("Gemini", gemini_api_key)
        st.sidebar.success("Gemini API Key saved!")

    perplexity_api_key_from_file = api_keys.load_api_key("Perplexity")
    perplexity_api_key = st.sidebar.text_input("Perplexity API Key", value=perplexity_api_key_from_file, type="password")
    if perplexity_api_key and perplexity_api_key != perplexity_api_key_from_file:
        api_keys.save_api_key("Perplexity", perplexity_api_key)
        st.sidebar.success("Perplexity API Key saved!")


    # File Uploads
    st.sidebar.title("Upload Your Documents")
    
    # Resume
    if st.session_state.resume_path:
        st.sidebar.info(f"Using cached resume: {os.path.basename(st.session_state.resume_path)}")
    resume = st.sidebar.file_uploader("Upload New Resume", type=["pdf"])
    if resume:
        st.session_state.resume_path = file_operations.cache_user_file(resume, "resume")
        st.sidebar.success("New resume cached!")

    # Job Description
    if st.session_state.jd_path:
        st.sidebar.info(f"Using cached JD: {os.path.basename(st.session_state.jd_path)}")
    ideal_jd = st.sidebar.file_uploader("Upload New Ideal Job Description", type=["pdf"])
    if ideal_jd:
        st.session_state.jd_path = file_operations.cache_user_file(ideal_jd, "jd")
        st.sidebar.success("New JD cached!")

    # LaTeX Template
    if st.session_state.latex_template_path:
        st.sidebar.info(f"Using cached LaTeX template: {os.path.basename(st.session_state.latex_template_path)}")
    latex_template = st.sidebar.file_uploader("Upload New LaTeX Resume Template", type=["tex"])
    if latex_template:
        st.session_state.latex_template_path = file_operations.cache_user_file(latex_template, "template")
        st.sidebar.success("New LaTeX template cached!")


    if st.sidebar.button("Analyze and Search for Jobs"):
        if st.session_state.resume_path and st.session_state.jd_path and gemini_api_key and perplexity_api_key:
            with st.spinner("Analyzing documents and searching for jobs..."):
                try:
                    # Step 1: Analysis
                    resume_text = file_operations.extract_text_from_file(st.session_state.resume_path)
                    jd_text = file_operations.extract_text_from_file(st.session_state.jd_path)

                    st.session_state.resume_analysis = resume_analyzer.analyze_resume(resume_text, gemini_api_key, "Gemini")
                    st.session_state.jd_analysis = jd_analyzer.analyze_jd(jd_text, gemini_api_key, "Gemini")
                    
                    # Step 2: Job Search
                    new_jobs = job_search.search_for_jobs(st.session_state.resume_analysis, st.session_state.jd_analysis, perplexity_api_key, gemini_api_key, resume_text, jd_text)
                    
                    cached_jobs = caching.get_cached_jobs()
                    cached_urls = {job['url'] for job in cached_jobs}
                    unique_new_jobs = [job for job in new_jobs if job.get('url') not in cached_urls]

                    if unique_new_jobs:
                        caching.add_to_cache(unique_new_jobs)
                        st.session_state.found_jobs = unique_new_jobs
                    else:
                        st.session_state.found_jobs = []
                    
                    st.success("Analysis and job search complete!")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Display welcome message if no analysis has been done yet
    if st.session_state.resume_analysis is None:
        st.header("Welcome to the Job Search AI Assistant!")
        st.markdown("""
            This tool is designed to help you streamline your job search process. Here's how to get started:

            1.  **Upload Your Documents**: Use the sidebar to upload your resume, an ideal job description, and an optional LaTeX resume template. The tool will remember your files for the next session.
            2.  **Enter API Keys**: Provide your API keys for Gemini (for analysis) and Perplexity (for job searching).
            3.  **Analyze and Search**: Click the "Analyze and Search for Jobs" button. The tool will:
                -   Analyze your resume and the ideal job description.
                -   Perform a real-time web search for relevant job postings.
                -   Display the analysis and job results side-by-side.
            4.  **Generate Materials**: Once the search is complete, you can select a job from the results to generate a tailored resume and cover letter.
            5.  **Manage History**: You can view previously found jobs or clear your search history from the sidebar.
        """)

    # Display results in a two-column layout
    if st.session_state.resume_analysis and st.session_state.jd_analysis:
        col1, col2 = st.columns(2)


        with col1:
            st.header("Analysis Results")
            with st.expander("Resume Analysis", expanded=False):
                st.json(st.session_state.resume_analysis)
            
            with st.expander("Ideal Job Description Analysis", expanded=False):
                st.json(st.session_state.jd_analysis)
            
            gap_analysis_results = jd_analyzer.gap_analysis(st.session_state.resume_analysis, st.session_state.jd_analysis)
            with st.expander("Gap Analysis", expanded=False):
                st.json(gap_analysis_results)

            ats_analysis_results = resume_analyzer.ats_analysis(
                file_operations.extract_text_from_file(st.session_state.resume_path),
                file_operations.extract_text_from_file(st.session_state.jd_path),
                gemini_api_key, "Gemini"
            )
            with st.expander("ATS Analysis", expanded=False):
                st.json(ats_analysis_results)

        with col2:
            st.header("Job Search Results")
            if st.session_state.found_jobs:
                st.info(f"Found {len(st.session_state.found_jobs)} new jobs.")
                for job in st.session_state.found_jobs:
                    post_date_str = job.get('posted_date', 'N/A')
                    try:
                        post_date = datetime.fromisoformat(post_date_str)
                        date_str = post_date.strftime("%Y-%m-%d")
                        if (datetime.now() - post_date).days <= 7:
                            st.markdown(f"**{job.get('title', 'N/A')}** at {job.get('company', 'N/A')} - [Link]({job.get('url', '#')}) - <span style='color: #28a745;'>Posted: {date_str} (Recent)</span>", unsafe_allow_html=True)
                        else:
                            st.write(f"**{job.get('title', 'N/A')}** at {job.get('company', 'N/A')} - [Link]({job.get('url', '#')}) - Posted: {date_str}")
                    except (ValueError, TypeError):
                        st.write(f"**{job.get('title', 'N/A')}** at {job.get('company', 'N/A')} - [Link]({job.get('url', '#')}) - Posted: {post_date_str}")
            else:
                st.info("No new jobs found. Your cache is up to date.")

    # Cache Management in Sidebar
    st.sidebar.title("History")
    if st.sidebar.button("Clear History"):
        caching.clear_cache()
        st.sidebar.success("Job history cleared!")

    with st.sidebar.expander("View Cached Jobs"):
        cached_jobs = caching.get_cached_jobs()
        if cached_jobs:
            for job in cached_jobs:
                if st.button(f"Generate for: {job.get('title', 'N/A')} at {job.get('company', 'N/A')}", key=job.get('url')):
                    st.session_state.selected_jd_from_cache = job
        else:
            st.write("No jobs in history.")


    # Combine new and cached jobs for selection
    all_jobs_dict = {job.get('url'): job for job in st.session_state.found_jobs + caching.get_cached_jobs() if job.get('url')}
    all_selectable_jobs = list(all_jobs_dict.values())

    if all_selectable_jobs:
        job_options = {f"{job.get('title', 'N/A')} at {job.get('company', 'N/A')}": job for job in all_selectable_jobs}
        # Check if there are any jobs to select from before showing the selectbox
        if job_options:
            # Determine default selection from sidebar button click
            default_index = 0
            if 'selected_jd_from_cache' in st.session_state and st.session_state.selected_jd_from_cache:
                selected_job = st.session_state.selected_jd_from_cache
                selected_job_key = f"{selected_job.get('title', 'N/A')} at {selected_job.get('company', 'N/A')}"
                if selected_job_key in job_options:
                    default_index = list(job_options.keys()).index(selected_job_key)
                # Clear the state after using it to prevent it from being sticky
                st.session_state.selected_jd_from_cache = None

            selected_job_title = st.selectbox("Select a Job Description", list(job_options.keys()), index=default_index)
            selected_jd = job_options[selected_job_title]

            additional_context = st.text_area("Add any additional context or instructions for the AI:")

            if st.button("Generate"):
                # Ensure analysis is available before generating
                if not st.session_state.resume_analysis or not st.session_state.jd_analysis:
                    if st.session_state.resume_path and st.session_state.jd_path and gemini_api_key:
                        with st.spinner("Performing initial analysis..."):
                            try:
                                resume_text = file_operations.extract_text_from_file(st.session_state.resume_path)
                                jd_text = file_operations.extract_text_from_file(st.session_state.jd_path)
                                st.session_state.resume_analysis = resume_analyzer.analyze_resume(resume_text, gemini_api_key, "Gemini")
                                st.session_state.jd_analysis = jd_analyzer.analyze_jd(jd_text, gemini_api_key, "Gemini")
                            except Exception as e:
                                st.error(f"Analysis failed: {e}")
                                st.stop() # Stop if analysis fails
                    else:
                        st.warning("Please upload a resume and ideal JD before generating.")
                        st.stop()

                if selected_jd:
                    st.info(f"Generating application materials for: **{selected_jd.get('title', 'N/A')}** at **{selected_jd.get('company', 'N/A')}**")
                    with st.spinner("Generating resume and cover letter..."):
                        try:
                            genai.configure(api_key=gemini_api_key)
                            model = genai.GenerativeModel('gemini-2.5-pro')

                            resume_text = file_operations.extract_text_from_file(st.session_state.resume_path)
                            
                            with st.expander("Analysis Summary", expanded=False):
                                st.write("#### Strengths")
                                st.write(st.session_state.resume_analysis.get('strengths', 'N/A'))
                                st.write("#### Areas for Development")
                                st.write(st.session_state.resume_analysis.get('areas_for_development', 'N/A'))
                                st.write("#### Gaps")
                                st.write(jd_analyzer.gap_analysis(st.session_state.resume_analysis, st.session_state.jd_analysis).get('missing_skills', 'N/A'))

                            # Generate Resume
                            latex_template_text = ""
                            if st.session_state.latex_template_path:
                                with open(st.session_state.latex_template_path, "r") as f:
                                    latex_template_text = f.read()
                            else:
                                latex_template_text = """
                                \\documentclass{article}
                                \\usepackage{fullpage}
                                \\begin{document}
                                \\title{Your Name}
                                \\author{Your Contact Information}
                                \\date{}
                                \\maketitle
                                \\section*{Summary}
                                % Your summary here
                                \\section*{Experience}
                                % Your experience here
                                \\section*{Education}
                                % Your education here
                                \\section*{Skills}
                                % Your skills here
                                \\end{document}
                                """

                            resume_prompt = f"""
                            Based on the following resume, the selected job description, and any additional context, generate an improved resume in LaTeX format.
                            Use the provided LaTeX template as a base. The generated resume should be tailored to the job description,
                            highlighting the most relevant skills and experience.

                            Resume:
                            {resume_text}

                            Job Description:
                            {selected_jd.get('description', '')}

                            Additional Context:
                            {additional_context}

                            LaTeX Template:
                            {latex_template_text}
                            """
                            resume_response = model.generate_content(resume_prompt)
                            resume_latex = resume_response.text

                            # Generate summary of changes
                            summary_prompt = f"""
                            Based on the original resume and the generated LaTeX resume, provide a brief summary of the key changes made.
                            Focus on how the resume was tailored to the job description.

                            Original Resume:
                            {resume_text}

                            Generated Resume (LaTeX):
                            {resume_latex}
                            """
                            summary_model = genai.GenerativeModel('gemini-2.5-flash')
                            summary_response = summary_model.generate_content(summary_prompt)
                            summary_text = summary_response.text

                            # Before/After ATS Analysis
                            original_ats = resume_analyzer.ats_analysis(resume_text, selected_jd.get('description', ''), gemini_api_key, "Gemini")
                            new_resume_text = file_operations.extract_text_from_latex(resume_latex)
                            new_ats = resume_analyzer.ats_analysis(new_resume_text, selected_jd.get('description', ''), gemini_api_key, "Gemini")

                            st.write("### ATS Analysis Comparison")
                            
                            # Custom CSS for table width
                            st.markdown("""
                            <style>
                            .dataframe table {
                                width: 100% !important;
                            }
                            .dataframe th {
                                min-width: 150px; /* Adjust as needed */
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            st.table({
                                "Metric": ["ATS Score", "Keyword Match"],
                                "Before": [original_ats.get('ats_score', 'N/A'), ", ".join(original_ats.get('keywords_match', []))],
                                "After": [new_ats.get('ats_score', 'N/A'), ", ".join(new_ats.get('keywords_match', []))]
                            })

                            st.write("### Summary of Resume Changes")
                            st.write(summary_text)

                            # Generate Cover Letter
                            cover_letter_prompt = f"""
                            Based on the following resume, the selected job description, and any additional context, write a professional cover letter.

                            Resume:
                            {resume_text}

                            Job Description:
                            {selected_jd.get('description', '')}
                            
                            Additional Context:
                            {additional_context}
                            """
                            cover_letter_response = model.generate_content(cover_letter_prompt)
                            cover_letter_text = cover_letter_response.text

                            st.write("### Generated Resume (LaTeX)")
                            st.code(resume_latex, language='latex')
                            st.download_button("Download Resume (LaTeX)", resume_latex, "resume.tex")
                            
                            st.write("### Generated Cover Letter")
                            st.text(cover_letter_text)
                            st.download_button("Download Cover Letter", cover_letter_text, "cover_letter.txt")
                        except Exception as e:
                            st.error(f"An error occurred during generation: {e}")

if __name__ == "__main__":
    main()