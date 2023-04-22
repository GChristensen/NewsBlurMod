//
//  FeedDetailGridView.swift
//  NewsBlur
//
//  Created by David Sinclair on 2023-01-19.
//  Copyright © 2023 NewsBlur. All rights reserved.
//

import SwiftUI

/// A protocol of interaction between a card in the grid, and the enclosing feed detail view controller.
protocol FeedDetailInteraction {
    var storyHeight: CGFloat { get }
    
    func pullToRefresh()
    func visible(story: Story)
    func tapped(story: Story)
    func reading(story: Story)
    func read(story: Story)
    func hid(story: Story)
}

/// A list or grid layout of story cards for the feed detail view.
struct FeedDetailGridView: View {
    var feedDetailInteraction: FeedDetailInteraction
    
    @ObservedObject var cache: StoryCache
    
    @State private var scrollOffset = CGPoint()
    
    let storyViewID = "storyViewID"
    
    var columns: [GridItem] {
        if cache.isGrid {
            return Array(repeating: GridItem(.flexible(), spacing: 20), count: cache.settings.gridColumns)
        } else {
            return [GridItem(.flexible())]
        }
    }
    
    var isOS15OrLater: Bool {
        if #available(iOS 15.0, *) {
            return true
        } else {
            return false
        }
    }
    
    var cardHeight: CGFloat {
        return cache.settings.gridHeight
    }
    
    var storyHeight: CGFloat {
        print("Story height: \(feedDetailInteraction.storyHeight + 20)")
        
        return feedDetailInteraction.storyHeight + 20
    }
    
    var body: some View {
        GeometryReader { reader in
            ScrollView {
                ScrollViewReader { scroller in
                    LazyVGrid(columns: columns, spacing: cache.isGrid ? 20 : 0) {
                        Section {
                            ForEach(cache.before, id: \.id) { story in
                                makeCardView(for: story, cache: cache, reader: reader)
                            }
                        }
                        
                        if cache.isGrid && !cache.isPhone {
                            EmptyView()
                                .id(storyViewID)
                        } else if let story = cache.selected {
                            makeCardView(for: story, cache: cache, reader: reader)
                                .id(story.id)
                        }
                        
                        Section(header: makeStoryView(cache: cache)) {
                            ForEach(cache.after, id: \.id) { story in
                                makeCardView(for: story, cache: cache, reader: reader)
                            }
                        }
                        
                        makeLoadingView(cache: cache)
                    }
                    .onChange(of: cache.selected) { [oldSelected = cache.selected] newSelected in
                        guard let newSelected, oldSelected?.hash != newSelected.hash else {
                            return
                        }
                        
                        print("\(oldSelected?.title ?? "none") -> \(newSelected.title)")
                        
                        Task {
                            if cache.isGrid {
                                withAnimation(Animation.spring().delay(0.5)) {
                                    scroller.scrollTo(storyViewID, anchor: .top)
                                }
                            } else {
                                withAnimation(Animation.spring().delay(0.5)) {
                                    scroller.scrollTo(newSelected.id)
                                }
                            }
                        }
                    }
                    .onAppear() {
                        if cache.isGrid {
                            scroller.scrollTo(storyViewID, anchor: .top)
                        }
                    }
                    .if(cache.isGrid) { view in
                        view.padding()
                    }
                }
            }
            .modify({ view in
                if #available(iOS 15.0, *) {
                    view.refreshable {
                        if cache.canPullToRefresh {
                            feedDetailInteraction.pullToRefresh()
                        }
                    }
                }
            })
        }
        .background(Color.themed([0xF4F4F4, 0xFFFDEF, 0x4F4F4F, 0x101010]))
    }
    
    @ViewBuilder
    func makeCardView(for story: Story, cache: StoryCache, reader: GeometryProxy) -> some View {
        CardView(feedDetailInteraction: feedDetailInteraction, cache: cache, story: loaded(story: story))
            .transformAnchorPreference(key: CardKey.self, value: .bounds) {
                $0.append(CardFrame(id: "\(story.id)", frame: reader[$1]))
            }
            .onPreferenceChange(CardKey.self) {
                print("pref change for '\(story.title)': \($0)")
                
                if let value = $0.first, value.frame.minY < -(value.frame.size.height / 2) {
                    print("pref '\(story.title)': scrolled off the top")
                    
                    feedDetailInteraction.read(story: story)
                }
            }
            .onAppear {
                feedDetailInteraction.visible(story: story)
            }
            .if(cache.isGrid) { view in
                view.frame(height: cardHeight)
            }
    }
    
    @ViewBuilder
    func makeStoryView(cache: StoryCache) -> some View {
        if cache.isGrid, !cache.isPhone, let story = cache.selected {
            StoryView(cache: cache, story: loaded(story: story), interaction: feedDetailInteraction)
        }
    }
    
    @ViewBuilder
    func makeLoadingView(cache: StoryCache) -> some View {
        ProgressView()
            .progressViewStyle(CircularProgressViewStyle(tint: cache.isDarkTheme ? .white : .black))
            .scaleEffect(2)
            .frame(height: 100)
    }
    
    func loaded(story: Story) -> Story {
        story.load()
        
        print("Loaded story '\(story.title)")
        
        return story
    }
}

struct CardFrame : Equatable {
    let id : String
    let frame : CGRect
    
    static func == (lhs: CardFrame, rhs: CardFrame) -> Bool {
        lhs.id == rhs.id && lhs.frame == rhs.frame
    }
}

struct CardKey : PreferenceKey {
    typealias Value = [CardFrame]
    
    static var defaultValue: [CardFrame] = []
    
    static func reduce(value: inout [CardFrame], nextValue: () -> [CardFrame]) {
        value.append(contentsOf: nextValue())
    }
}
