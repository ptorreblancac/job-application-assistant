
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, test, expect, beforeEach, vi } from 'vitest'
import App from '../App'

const mockProfile = {
    id: 1,
    target_role: 'Software Engineer',
    location: 'Barcelona',
    country: 'Spain',
    seniority: 'Graduate',
    work_arrangements: ['Remote', 'Hybrid'],
    preferred_skills: ['Python', 'React', 'Django']
}

const mockJobs = [
    {
        id: 1,
        title: 'Junior Software Engineer',
        company: 'Google',
        location: 'Barcelona',
        job_type: 'Full-time',
        relevance_score: 85,
        date_posted: '2026-11-20',
        posting_link: 'https://example.com/1',
        description: 'Software development with Python'
    },
    {
        id: 2,
        title: 'Frontend Developer',
        company: 'Amazon',
        location: 'Madrid',
        job_type: 'Part-time',
        relevance_score: 75,
        date_posted: '2026-11-22',
        posting_link: 'https://example.com/2',
        description: 'React and JavaScript development'
    }
]

describe('App', () => {

    beforeEach(() => {
        vi.stubGlobal('fetch', vi.fn((url) => {

            if (url === 'http://127.0.0.1:8000/jobs/') {
                return Promise.resolve({
                    ok: true,
                    json: async () => mockJobs
                })
            }

            if (url === 'http://127.0.0.1:8000/jobs/profiles/1/') {
                return Promise.resolve({
                    ok: true,
                    json: async () => mockProfile
                })
            }

            if (url === 'http://127.0.0.1:8000/jobs/profiles/1/update/') {
                return Promise.resolve({
                    ok: true,
                    text: async () => JSON.stringify(mockProfile)
                })
            }

            return Promise.reject(new Error('Unexpected API request'))
        }))
    })

    test('displays the dashboard by default', async () => {
        render(<App />)

        expect(await screen.findByText('Recommended Jobs')).toBeInTheDocument()
        expect(screen.getAllByText('Junior Software Engineer')).toHaveLength(2)
    })

    test('navigates to the Job Search page', async () => {
        const user = userEvent.setup()
        render(<App />)

        await user.click(screen.getByText('Job Search'))

        expect(
            screen.getByText('Explore and discover opportunities matching your profile.')
        ).toBeInTheDocument()

        expect(screen.getByText('Junior Software Engineer')).toBeInTheDocument()
    })

    test('navigates to the Profile page', async () => {
        const user = userEvent.setup()
        render(<App />)

        await user.click(screen.getByText('Profile'))

        expect(
            await screen.findByDisplayValue('Software Engineer')
        ).toBeInTheDocument()

        expect(screen.getByDisplayValue('Barcelona')).toBeInTheDocument()
    })

    test('can navigate between all three pages', async () => {
        const user = userEvent.setup()
        render(<App />)

        // Dashboard → Job Search
        expect(await screen.findByText('Recommended Jobs')).toBeInTheDocument()

        await user.click(screen.getByText('Job Search'))

        expect(
            screen.getByText('Explore and discover opportunities matching your profile.')
        ).toBeInTheDocument()

        // Job Search → Profile
        await user.click(screen.getByText('Profile'))

        expect(
            await screen.findByDisplayValue('Software Engineer')
        ).toBeInTheDocument()

        // Profile → Dashboard
        await user.click(screen.getByRole('link', { name: 'Dashboard' }))

        expect(await screen.findByText('Recommended Jobs')).toBeInTheDocument()
    })

    test('allows the user to edit and save their profile', async () => {
        const user = userEvent.setup()
        render(<App />)

        // Navigate to Profile
        await user.click(screen.getByRole('link', { name: 'Profile' }))

        // Wait for the profile to load
        const targetRoleInput = await screen.findByDisplayValue('Software Engineer')

        // Edit the target role
        await user.clear(targetRoleInput)
        await user.type(targetRoleInput, 'Backend Developer')

        // Save changes
        await user.click(screen.getByRole('button', { name: 'Save changes' }))

        // Verify success message
        expect(await screen.findByText(/profile saved successfully/i)).toBeInTheDocument()

        // Verify the PUT request
        const putCall = fetch.mock.calls.find(
            call => call[1]?.method === 'PUT'
        )

        expect(putCall).toBeDefined()

        const requestBody = JSON.parse(putCall[1].body)

        expect(requestBody.target_role).toBe('Backend Developer')
    })

})
