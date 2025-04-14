sample_projects = [
    {
        'id': 'PRJ001',
        'name': 'Project Alpha',
        'description': 'A critical infrastructure upgrade project',
        'status': 'In Progress',
        'start_date': '2025-01-15',
        'end_date': '2025-07-30',
        'budget': 1250000,
        'spent': 450000,
        'team_size': 12,
        'risk_score': 7.8,
        'risk_delta': 1.2,
        'schedule_risk': 8.5,
        'budget_risk': 6.2,
        'resource_risk': 7.1,
        'market_risk': 5.8,
        'technical_risk': 8.3,
        'risk_factors': [
            {
                'name': 'Supply Chain Delays',
                'description': 'Shipping delays due to global logistics',
                'category': 'schedule_risk',
                'impact': 9,
                'likelihood': 7,
                'mitigation': 'Use alternative suppliers and buffer inventory'
            },
            {
                'name': 'Legacy System Integration',
                'description': 'Complex integration with old systems',
                'category': 'technical_risk',
                'impact': 8,
                'likelihood': 9,
                'mitigation': 'Assign senior devs, conduct early testing'
            }
        ],
        'risk_history': [
            {'date': '2025-01-15', 'risk_score': 5.2},
            {'date': '2025-02-15', 'risk_score': 6.1},
            {'date': '2025-03-15', 'risk_score': 6.6},
            {'date': '2025-04-11', 'risk_score': 7.8}
        ]
    },
    {
        'id': 'PRJ002',
        'name': 'Project Beta',
        'description': 'New product development for healthcare sector',
        'status': 'On Track',
        'start_date': '2025-02-01',
        'end_date': '2025-10-31',
        'budget': 980000,
        'spent': 310000,
        'team_size': 8,
        'risk_score': 4.2,
        'risk_delta': -0.5,
        'schedule_risk': 3.8,
        'budget_risk': 4.5,
        'resource_risk': 3.9,
        'market_risk': 6.1,
        'technical_risk': 4.8,
        'risk_factors': [
            {
                'name': 'Regulatory Approval',
                'description': 'Risk of delays in obtaining approvals',
                'category': 'market_risk',
                'impact': 8,
                'likelihood': 5,
                'mitigation': 'Hire regulatory consultants early'
            }
        ],
        'risk_history': [
            {'date': '2025-02-01', 'risk_score': 4.8},
            {'date': '2025-03-01', 'risk_score': 5.1},
            {'date': '2025-04-01', 'risk_score': 4.2}
        ]
    },
    {
        'id': 'PRJ003',
        'name': 'Project Gamma',
        'description': 'Digital transformation for finance operations',
        'status': 'At Risk',
        'start_date': '2024-11-01',
        'end_date': '2025-06-30',
        'budget': 1850000,
        'spent': 950000,
        'team_size': 15,
        'risk_score': 8.9,
        'risk_delta': 2.1,
        'schedule_risk': 9.2,
        'budget_risk': 8.7,
        'resource_risk': 7.6,
        'market_risk': 4.5,
        'technical_risk': 9.1,
        'risk_factors': [
            {
                'name': 'Budget Overruns',
                'description': 'Scope changes affecting budget',
                'category': 'budget_risk',
                'impact': 9,
                'likelihood': 8,
                'mitigation': 'Use change control and re-scoping'
            },
            {
                'name': 'System Integration Issues',
                'description': 'Legacy integration causing delays',
                'category': 'technical_risk',
                'impact': 8,
                'likelihood': 9,
                'mitigation': 'Use vendor support and phased approach'
            }
        ],
        'risk_history': [
            {'date': '2024-11-01', 'risk_score': 5.3},
            {'date': '2025-01-01', 'risk_score': 7.1},
            {'date': '2025-04-01', 'risk_score': 8.9}
        ]
    }
]
